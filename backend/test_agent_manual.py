import asyncio
from app.agent.graph import agent_app

async def main():
    print("Testing Agent...")
    inputs = {"user_input": "Show me the total fees paid in SOL in the last 24 hours"}
    
    result = await agent_app.ainvoke(inputs)
    
    print("\nSQL Generated:")
    print(result["sql_output"])

if __name__ == "__main__":
    asyncio.run(main())
