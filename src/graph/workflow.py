from langgraph.graph import StateGraph, START, END
from config.settings import CONFIDENCE_THRESHOLD, MAX_RETRIES
from src.graph.state import ResearchState
from src.agents.nodes import researcher_node, summarizer_node, factcheck_node

def should_retry(state:ResearchState)->str:
    """
    evaluate whether the research needs to be repeated based on the fact check confidence score and retry limits
    """
    score=state.get("fact_check_score",0.0)
    retry_count=state.get("retry_count",0)

    print(f"\n[router]:checking {score} (threshold:{CONFIDENCE_THRESHOLD}) | retry: {retry_count} {MAX_RETRIES}")
    if score >= CONFIDENCE_THRESHOLD or retry_count>=MAX_RETRIES:
        print("[router]:Finishing workflow")
        return "end"
    else:
        print("[router]:score below thereshold. retrying the research.")
        return "retry"

def build_research_graph():
    """
        construct and complile the multiagent graph workflow
    """
    workflow=StateGraph(ResearchState)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("factchecker", factcheck_node)

    workflow.add_edge(START,"researcher")
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", "factchecker")

    workflow.add_conditional_edges("factchecker",should_retry,{"retry":"researcher","end":END})

    return workflow.compile()

app=build_research_graph()