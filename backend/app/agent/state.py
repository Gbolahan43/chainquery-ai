from typing import TypedDict, Optional

class AgentState(TypedDict):
    """
    Defines the input/output structure for our graph.
    """
    user_input: str          # What the user asked
    sql_output: Optional[str] # The generated SQL
    error: Optional[str]      # If something goes wrong
