"""
Agent workflow module - exports the compiled LangGraph agent
"""
from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import generate_sql

# 1. Initialize the Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("generator", generate_sql)

# 3. Define Edges (The Flow)
# Start -> Generator -> End
workflow.set_entry_point("generator")
workflow.add_edge("generator", END)

# 4. Compile the Graph
agent_app = workflow.compile()
