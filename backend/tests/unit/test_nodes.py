"""
Unit tests for agent nodes module
Tests SQL generation node functionality with mocked LLM
"""
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.agent.state import AgentState
from app.agent.nodes import generate_sql


class TestGenerateSQLNode:
    """Test generate_sql node function"""
    
    @pytest.mark.asyncio
    async def test_generate_sql_success(self):
        """Test successful SQL generation"""
        # Mock state
        state = {
            "user_input": "Show me top 10 SOL holders",
            "chain": "solana"
        }
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "SELECT * FROM solana_utils.latest_balances WHERE token_mint_address IS NULL ORDER BY sol_balance DESC LIMIT 10;"
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            
            result = await generate_sql(state)
            
            assert result is not None
            assert "sql_output" in result
            assert "error" in result
            assert result["error"] is None
            assert result["sql_output"] is not None
            assert "SELECT" in result["sql_output"]
    
    @pytest.mark.asyncio
    async def test_generate_sql_removes_markdown(self):
        """Test that markdown backticks are removed from SQL"""
        state = {
            "user_input": "Get USDC volume",
            "chain": "solana"
        }
        
        # Mock response with markdown
        mock_response = MagicMock()
        mock_response.content = "```sql\nSELECT COUNT(*) FROM solana.transactions;\n```"
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            
            result = await generate_sql(state)
            
            # Should remove ```sql and ```
            assert "```" not in result["sql_output"]
            assert "SELECT" in result["sql_output"]
    
    @pytest.mark.asyncio
    async def test_generate_sql_handles_error(self):
        """Test error handling when LLM call fails"""
        state = {
            "user_input": "Test query",
            "chain": "solana"
        }
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(side_effect=Exception("API Error"))
            
            result = await generate_sql(state)
            
            assert result is not None
            assert "sql_output" in result
            assert "error" in result
            assert result["sql_output"] is None
            assert result["error"] == "API Error"
    
    @pytest.mark.asyncio
    async def test_generate_sql_passes_user_input(self):
        """Test that user input is correctly passed to LLM"""
        user_input = "Show daily USDC transfers"
        state = {
            "user_input": user_input,
            "chain": "solana"
        }
        
        mock_response = MagicMock()
        mock_response.content = "SELECT * FROM solana.account_activity;"
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            
            await generate_sql(state)
            
            # Verify ainvoke was called
            mock_llm.ainvoke.assert_called_once()
            
            # Check that messages were passed
            call_args = mock_llm.ainvoke.call_args[0][0]
            assert len(call_args) == 2  # SystemMessage and HumanMessage
            assert call_args[1].content == user_input
    
    @pytest.mark.asyncio
    async def test_generate_sql_includes_system_prompt(self):
        """Test that system prompt is included in LLM call"""
        state = {
            "user_input": "Test",
            "chain": "solana"
        }
        
        mock_response = MagicMock()
        mock_response.content = "SELECT 1;"
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            
            await generate_sql(state)
            
            # Get the messages passed to LLM
            call_args = mock_llm.ainvoke.call_args[0][0]
            
            # First message should be SystemMessage
            assert call_args[0].__class__.__name__ == "SystemMessage"
            # Second should be HumanMessage
            assert call_args[1].__class__.__name__ == "HumanMessage"
    
    @pytest.mark.asyncio
    async def test_generate_sql_strips_whitespace(self):
        """Test that output SQL is stripped of extra whitespace"""
        state = {
            "user_input": "Get data",
            "chain": "solana"
        }
        
        mock_response = MagicMock()
        mock_response.content = "  \n  SELECT * FROM table;  \n  "
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            
            result = await generate_sql(state)
            
            # Should be stripped
            assert not result["sql_output"].startswith(" ")
            assert not result["sql_output"].endswith(" ")
            assert not result["sql_output"].startswith("\n")
    
    @pytest.mark.asyncio
    async def test_generate_sql_empty_input(self):
        """Test handling of empty user input"""
        state = {
            "user_input": "",
            "chain": "solana"
        }
        
        mock_response = MagicMock()
        mock_response.content = "SELECT 1;"
        
        with patch('app.agent.nodes.llm') as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            
            result = await generate_sql(state)
            
            # Should still process (validation happens elsewhere)
            assert result is not None
            assert "sql_output" in result
