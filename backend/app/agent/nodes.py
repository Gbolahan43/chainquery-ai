from langchain_aws import ChatBedrock
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT

# Prepare AWS credentials safely (only pass if they exist)
aws_credentials = {}
if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
    aws_credentials = {
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
    }

# Primary LLM: AWS Bedrock (Claude 4.5 Sonnet)
bedrock_llm = ChatBedrock(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",  
    region_name=settings.AWS_DEFAULT_REGION,
    model_kwargs={"temperature": 0},
    **aws_credentials
)

# Fallback LLM: Groq (Llama 3.3 70B)
groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",  
    api_key=settings.GROQ_API_KEY,
    temperature=0
)

# Combine with LangChain's fallback mechanism
llm = bedrock_llm.with_fallbacks([groq_llm])

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
        content = response.content
        
        # Extract SQL from <sql> tags if present (Chain of Thought format)
        import re
        sql_match = re.search(r"<sql>(.*?)</sql>", content, re.DOTALL | re.IGNORECASE)
        
        if sql_match:
            clean_sql = sql_match.group(1).strip()
        else:
            # Fallback if the model ignores instructions
            clean_sql = content.replace("```sql", "").replace("```", "").strip()
        
        return {"sql_output": clean_sql, "error": None}
        
    except Exception as e:
        return {"sql_output": None, "error": str(e)}
