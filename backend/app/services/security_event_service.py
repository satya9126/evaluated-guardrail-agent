import uuid

from sqlalchemy.orm import Session

from app.database.models import SecurityEvent


def save_security_event(
    db: Session,
    prompt_injection_detected: bool,
    pii_detected: bool,
    model_used: str,
    response_status: str,
):
    event = SecurityEvent(
        request_id=str(uuid.uuid4()),
        prompt_injection_detected=prompt_injection_detected,
        pii_detected=pii_detected,
        model_used=model_used,
        response_status=response_status,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event