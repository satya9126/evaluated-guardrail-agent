from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.llm_service import LLMService
from app.guardrails.prompt_injection import PromptInjectionGuard
from app.guardrails.pii_detector import PIIDetector
from app.guardrails.output_guardrail import OutputGuardrail
from app.agents.graph import build_graph
from app.database.connection import get_db
from app.services.security_event_service import save_security_event
from app.redis.rate_limiter import check_rate_limit
from app.auth.dependencies import get_current_user


router = APIRouter()

llm = LLMService()
prompt_guard = PromptInjectionGuard()
pii_detector = PIIDetector()
output_guard = OutputGuardrail()

agent_graph = build_graph()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(
    request: ChatRequest,
    http_request: Request,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # -----------------------------
    # 1. Redis Rate Limiting
    # -----------------------------
    check_rate_limit(http_request)

    # -----------------------------
    # 2. Prompt Injection Guard
    # -----------------------------
    is_safe = prompt_guard.check(request.message)

    if not is_safe:
        save_security_event(
            db=db,
            prompt_injection_detected=True,
            pii_detected=False,
            model_used="openai",
            response_status="blocked_prompt_injection"
        )

        raise HTTPException(
            status_code=400,
            detail="Potential prompt injection detected."
        )

    # -----------------------------
    # 3. PII Detection & Redaction
    # -----------------------------
    original_message = request.message

    safe_message = pii_detector.detect_and_redact(
        original_message
    )

    pii_detected = safe_message != original_message

    # -----------------------------
    # 4. LangGraph Processing
    # -----------------------------
    result = agent_graph.invoke(
        {
            "message": safe_message,
            "response": ""
        }
    )

    response = result["response"]

    # -----------------------------
    # 5. Output Guardrail
    # -----------------------------
    output_allowed, safe_response = output_guard.check(
        response
    )

    if not output_allowed:
        save_security_event(
            db=db,
            prompt_injection_detected=False,
            pii_detected=pii_detected,
            model_used="openai",
            response_status="blocked_output"
        )

        raise HTTPException(
            status_code=400,
            detail=safe_response
        )

    # -----------------------------
    # 6. Save Security Event
    # -----------------------------
    save_security_event(
        db=db,
        prompt_injection_detected=False,
        pii_detected=pii_detected,
        model_used="openai",
        response_status="success"
    )

    # -----------------------------
    # 7. Return Response
    # -----------------------------
    return {
        "response": safe_response
    }