from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from agents.supervisor import supervisor_node
from agents.researcher import researcher_node
from agents.analyst import analyst_node
from agents.editor import editor_node

workflow = StateGraph(AgentState)

workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Researcher", researcher_node)
workflow.add_node("Analyst", analyst_node)
workflow.add_node("Editor", editor_node)

workflow.add_edge("Researcher", "Supervisor")
workflow.add_edge("Analyst", "Supervisor")
workflow.add_edge("Editor", "Supervisor")

workflow.add_conditional_edges(
    "Supervisor",
    lambda state: state["next"],
    {
        "Researcher": "Researcher",
        "Analyst": "Analyst",
        "Editor": "Editor",
        "FINISH": END
    }
)

workflow.add_edge(START, "Supervisor")

app = workflow.compile()