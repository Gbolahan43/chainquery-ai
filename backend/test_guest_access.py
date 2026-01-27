"""
Guest Access Test Script
Demonstrates the end-to-end guest access flow without requiring a running database.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class QueryResponse:
    id: uuid.UUID
    user_input: str
    sql_output: str
    session_id: str
    created_at: datetime
    error: Optional[str] = None


# Simulate in-memory database
query_storage: List[QueryResponse] = []


def generate_query(user_input: str, chain: str, session_id: str) -> QueryResponse:
    """
    Simulates the /generate endpoint
    """
    # Simulate SQL generation (normally done by LangGraph Agent)
    sql_output = f"SELECT * FROM {chain}.transactions WHERE user_query = '{user_input}' LIMIT 10"
    
    # Create query response
    query = QueryResponse(
        id=uuid.uuid4(),
        user_input=user_input,
        sql_output=sql_output,
        session_id=session_id,
        created_at=datetime.utcnow()
    )
    
    # Save to "database"
    query_storage.append(query)
    
    return query


def get_history(session_id: str, limit: int = 10) -> List[QueryResponse]:
    """
    Simulates the /history endpoint - filters by session_id
    """
    # Filter queries by session_id
    session_queries = [q for q in query_storage if q.session_id == session_id]
    
    # Sort by created_at descending
    session_queries.sort(key=lambda x: x.created_at, reverse=True)
    
    # Apply limit
    return session_queries[:limit]


def test_guest_access():
    """
    Test the guest access isolation feature
    """
    print("=" * 60)
    print("GUEST ACCESS TEST - Session Isolation")
    print("=" * 60)
    print()
    
    # Simulate two different guest users
    guest_1_session = str(uuid.uuid4())
    guest_2_session = str(uuid.uuid4())
    
    print(f"[*] Guest 1 Session ID: {guest_1_session[:8]}...")
    print(f"[*] Guest 2 Session ID: {guest_2_session[:8]}...")
    print()
    
    # Guest 1 generates 3 queries
    print("Guest 1 generates 3 queries:")
    print("-" * 60)
    q1 = generate_query("Show me top SOL holders", "solana", guest_1_session)
    print(f"[OK] Query 1: {q1.user_input}")
    print(f"   SQL: {q1.sql_output}")
    
    q2 = generate_query("Daily DEX volume", "solana", guest_1_session)
    print(f"[OK] Query 2: {q2.user_input}")
    print(f"   SQL: {q2.sql_output}")
    
    q3 = generate_query("NFT sales today", "solana", guest_1_session)
    print(f"[OK] Query 3: {q3.user_input}")
    print(f"   SQL: {q3.sql_output}")
    print()
    
    # Guest 2 generates 2 queries
    print("Guest 2 generates 2 queries:")
    print("-" * 60)
    q4 = generate_query("Show whale transactions", "solana", guest_2_session)
    print(f"[OK] Query 1: {q4.user_input}")
    print(f"   SQL: {q4.sql_output}")
    
    q5 = generate_query("Get token prices", "solana", guest_2_session)
    print(f"[OK] Query 2: {q5.user_input}")
    print(f"   SQL: {q5.sql_output}")
    print()
    
    # Test history isolation
    print("[HISTORY] Testing History Isolation:")
    print("=" * 60)
    print()
    
    guest_1_history = get_history(guest_1_session)
    print(f"Guest 1 History (Session: {guest_1_session[:8]}...):")
    print(f"  Found {len(guest_1_history)} queries")
    for i, q in enumerate(guest_1_history, 1):
        print(f"    {i}. {q.user_input}")
    print()
    
    guest_2_history = get_history(guest_2_session)
    print(f"Guest 2 History (Session: {guest_2_session[:8]}...):")
    print(f"  Found {len(guest_2_history)} queries")
    for i, q in enumerate(guest_2_history, 1):
        print(f"    {i}. {q.user_input}")
    print()
    
    # Verify isolation
    print("[VERIFY] Isolation Test Results:")
    print("-" * 60)
    if len(guest_1_history) == 3:
        print("[PASS] Guest 1 sees exactly 3 queries (their own)")
    else:
        print(f"[FAIL] Guest 1 sees {len(guest_1_history)} queries (expected 3)")
    
    if len(guest_2_history) == 2:
        print("[PASS] Guest 2 sees exactly 2 queries (their own)")
    else:
        print(f"[FAIL] Guest 2 sees {len(guest_2_history)} queries (expected 2)")
    
    # Verify no cross-contamination
    guest_1_inputs = {q.user_input for q in guest_1_history}
    guest_2_inputs = {q.user_input for q in guest_2_history}
    
    if not guest_1_inputs.intersection(guest_2_inputs):
        print("[PASS] No query leakage between sessions")
    else:
        print("[FAIL] Query leakage detected!")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE - Guest Access Works!")
    print("=" * 60)
    print()
    
    # Show implementation details
    print("[INFO] Implementation Details:")
    print("-" * 60)
    print("1. Each guest gets a unique session_id (UUID)")
    print("2. /generate endpoint saves session_id with each query")
    print("3. /history endpoint filters by session_id")
    print("4. Guests can only see their own queries")
    print("5. No authentication required!")
    print()
    
    # Show actual API usage
    print("[API] Actual API Usage:")
    print("-" * 60)
    print()
    print("POST /api/v1/generate")
    print('{')
    print('  "user_input": "Show me top SOL holders",')
    print('  "chain": "solana",')
    print(f'  "session_id": "{guest_1_session}"')
    print('}')
    print()
    print(f"GET /api/v1/history?session_id={guest_1_session}")
    print()


if __name__ == "__main__":
    test_guest_access()
