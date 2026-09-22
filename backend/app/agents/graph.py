from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.agents.nodes import (
    process_request,
    generate_response
)


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node(
        "process_request",
        process_request
    )

    graph.add_node(
        "generate_response",
        generate_response
    )

    graph.add_edge(
        START,
        "process_request"
    )

    graph.add_edge(
        "process_request",
        "generate_response"
    )

    graph.add_edge(
        "generate_response",
        END
    )

    return graph.compile()