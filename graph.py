# graph.py
from langgraph.graph import StateGraph, START, END
from nodes.extraction import extraction_node
from nodes.retrieval import retrieval_node
from nodes.analysis import analysis_node
from models.schemas import PipelineState


def build_graph():
    """
    Build and compile the LangGraph pipeline.

    Returns:
        Compiled LangGraph workflow ready to be invoked.
    """
    workflow = StateGraph(PipelineState)

    workflow.add_node("extraction", extraction_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("analysis", analysis_node)

    workflow.add_edge(START, "extraction")
    workflow.add_edge("extraction", "retrieval")
    workflow.add_edge("retrieval", "analysis")
    workflow.add_edge("analysis", END)

    return workflow.compile()
