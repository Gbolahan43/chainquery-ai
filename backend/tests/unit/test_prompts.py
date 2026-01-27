"""
Unit tests for agent prompts module
Tests prompt content, structure, and key requirements
"""
import pytest
from app.agent.prompts import SYSTEM_PROMPT


class TestSystemPrompt:
    """Test SYSTEM_PROMPT content and structure"""
    
    def test_prompt_exists(self):
        """Test that SYSTEM_PROMPT is defined and not empty"""
        assert SYSTEM_PROMPT is not None
        assert len(SYSTEM_PROMPT) > 0
        assert isinstance(SYSTEM_PROMPT, str)
    
    def test_prompt_contains_critical_instructions(self):
        """Test that prompt contains critical SQL generation instructions"""
        # Must contain Trino/DuneSQL reference
        assert "Trino" in SYSTEM_PROMPT or "DuneSQL" in SYSTEM_PROMPT
        
        # Must mention time filter requirement
        assert "time filter" in SYSTEM_PROMPT.lower() or "block_time" in SYSTEM_PROMPT
        
        # Must have output format instructions
        assert "SELECT" in SYSTEM_PROMPT
        assert "semicolon" in SYSTEM_PROMPT.lower() or ";" in SYSTEM_PROMPT
    
    def test_prompt_contains_known_tokens(self):
        """Test that prompt includes known Solana tokens"""
        known_tokens = ["SOL", "USDC", "USDT", "JUP", "BONK"]
        
        for token in known_tokens:
            assert token in SYSTEM_PROMPT, f"Token {token} not found in SYSTEM_PROMPT"
    
    def test_prompt_contains_token_addresses(self):
        """Test that prompt includes actual token mint addresses"""
        # USDC mint address
        assert "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" in SYSTEM_PROMPT
        
        # USDT mint address
        assert "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB" in SYSTEM_PROMPT
        
        # JUP mint address
        assert "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN" in SYSTEM_PROMPT
    
    def test_prompt_contains_schema_tables(self):
        """Test that prompt includes Solana table schemas"""
        expected_tables = [
            "solana.transactions",
            "solana.instruction_calls",
            "solana.account_activity",
            "solana.rewards",
            "solana_utils.latest_balances"
        ]
        
        for table in expected_tables:
            assert table in SYSTEM_PROMPT, f"Table {table} not found in SYSTEM_PROMPT"
    
    def test_prompt_contains_schema_fields(self):
        """Test that prompt includes key schema fields"""
        critical_fields = [
            "block_time",
            "block_date",
            "signature",
            "signer",
            "fee",
            "success",
            "token_mint_address",
            "balance_change"
        ]
        
        for field in critical_fields:
            assert field in SYSTEM_PROMPT, f"Field {field} not found in SYSTEM_PROMPT"
    
    def test_prompt_contains_guidelines(self):
        """Test that prompt includes query generation guidelines"""
        assert "GUIDELINES" in SYSTEM_PROMPT.upper() or "RULES" in SYSTEM_PROMPT.upper()
        
        # Should mention joins
        assert "join" in SYSTEM_PROMPT.lower() or "JOIN" in SYSTEM_PROMPT
        
        # Should mention volume calculations
        assert "volume" in SYSTEM_PROMPT.lower() or "VOLUME" in SYSTEM_PROMPT
    
    def test_prompt_contains_examples(self):
        """Test that prompt includes few-shot examples"""
        # Should have example queries
        assert "example" in SYSTEM_PROMPT.lower() or "EXAMPLES" in SYSTEM_PROMPT.upper()
        
        # Should have sample SQL
        assert "SELECT" in SYSTEM_PROMPT and "FROM" in SYSTEM_PROMPT
    
    def test_prompt_format_instructions(self):
        """Test that prompt has clear format instructions"""
        # Should tell model not to use markdown
        assert "backticks" in SYSTEM_PROMPT.lower() or "```" in SYSTEM_PROMPT
        
        # Should tell model to output code only
        assert ("code only" in SYSTEM_PROMPT.lower() or 
                "strictly code" in SYSTEM_PROMPT.lower() or
                "directly with" in SYSTEM_PROMPT.lower())
    
    def test_prompt_contains_decimal_handling(self):
        """Test that prompt explains decimal/lamports conversion"""
        assert "lamports" in SYSTEM_PROMPT.lower()
        assert "1e9" in SYSTEM_PROMPT or "decimals" in SYSTEM_PROMPT.lower()
    
    def test_prompt_length_reasonable(self):
        """Test that prompt is substantial but not excessively long"""
        # Should be substantial (at least 2000 chars for comprehensive schema)
        assert len(SYSTEM_PROMPT) > 2000
        
        # But not excessively long (under 20000 chars)
        assert len(SYSTEM_PROMPT) < 20000
