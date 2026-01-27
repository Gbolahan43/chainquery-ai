from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT

# Initialize the LLM once
llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct", 
    api_key=settings.GROQ_API_KEY,
    temperature=0
)

async def generate_sql(state: AgentState) -> dict:
    """
    Node 1: Calls the LLM to convert User Input -> SQL
    """
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["user_input"])
        ]
        
        # Call the model asynchronously
        response = await llm.ainvoke(messages)
        
        # Clean up the output (remove markdown backticks if the model ignores instructions)
        clean_sql = response.content.replace("```sql", "").replace("```", "").strip()
        
        return {"sql_output": clean_sql, "error": None}
        
    except Exception as e:
        return {"sql_output": None, "error": str(e)}
