from app.services.llm_service import LLMService
from app.agents.state import AgentState


llm = LLMService()


def process_request(state: AgentState) -> AgentState:
    """
    Process the incoming user request.
    """

    message = state["message"].strip()

    return {
        **state,
        "message": message
    }


def generate_response(state: AgentState) -> AgentState:
    """
    Generate a response using the LLM.
    """

    response = llm.generate(
        state["message"]
    )

    return {
        **state,
        "response": response
    }