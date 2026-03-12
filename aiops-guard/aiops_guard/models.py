"""
Data models for AIOpsGuard
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class ModelPricing:
    """Pricing information for LLM models (USD per 1M tokens)"""
    
    # OpenAI GPT-4 models
    GPT_4_TURBO_INPUT: float = 10.00
    GPT_4_TURBO_OUTPUT: float = 30.00
    GPT_4_INPUT: float = 30.00
    GPT_4_OUTPUT: float = 60.00
    GPT_4_32K_INPUT: float = 60.00
    GPT_4_32K_OUTPUT: float = 120.00
    
    # OpenAI GPT-3.5 models
    GPT_3_5_TURBO_INPUT: float = 0.50
    GPT_3_5_TURBO_OUTPUT: float = 1.50
    GPT_3_5_TURBO_16K_INPUT: float = 3.00
    GPT_3_5_TURBO_16K_OUTPUT: float = 4.00
    
    # Anthropic Claude models
    CLAUDE_3_OPUS_INPUT: float = 15.00
    CLAUDE_3_OPUS_OUTPUT: float = 75.00
    CLAUDE_3_SONNET_INPUT: float = 3.00
    CLAUDE_3_SONNET_OUTPUT: float = 15.00
    CLAUDE_3_HAIKU_INPUT: float = 0.25
    CLAUDE_3_HAIKU_OUTPUT: float = 1.25
    
    @classmethod
    def get_pricing(cls, model_name: str) -> tuple[float, float]:
        """
        Get input and output pricing for a model
        
        Args:
            model_name: Name of the model
            
        Returns:
            Tuple of (input_price, output_price) per 1M tokens
        """
        model_lower = model_name.lower()
        
        # GPT-4 models
        if "gpt-4-turbo" in model_lower or "gpt-4-1106" in model_lower:
            return (cls.GPT_4_TURBO_INPUT, cls.GPT_4_TURBO_OUTPUT)
        elif "gpt-4-32k" in model_lower:
            return (cls.GPT_4_32K_INPUT, cls.GPT_4_32K_OUTPUT)
        elif "gpt-4" in model_lower:
            return (cls.GPT_4_INPUT, cls.GPT_4_OUTPUT)
        
        # GPT-3.5 models
        elif "gpt-3.5-turbo-16k" in model_lower:
            return (cls.GPT_3_5_TURBO_16K_INPUT, cls.GPT_3_5_TURBO_16K_OUTPUT)
        elif "gpt-3.5-turbo" in model_lower:
            return (cls.GPT_3_5_TURBO_INPUT, cls.GPT_3_5_TURBO_OUTPUT)
        
        # Claude models
        elif "claude-3-opus" in model_lower:
            return (cls.CLAUDE_3_OPUS_INPUT, cls.CLAUDE_3_OPUS_OUTPUT)
        elif "claude-3-sonnet" in model_lower:
            return (cls.CLAUDE_3_SONNET_INPUT, cls.CLAUDE_3_SONNET_OUTPUT)
        elif "claude-3-haiku" in model_lower:
            return (cls.CLAUDE_3_HAIKU_INPUT, cls.CLAUDE_3_HAIKU_OUTPUT)
        
        # Default to GPT-3.5 Turbo pricing
        return (cls.GPT_3_5_TURBO_INPUT, cls.GPT_3_5_TURBO_OUTPUT)


@dataclass
class CallMetrics:
    """Metrics for a single LLM call"""
    
    agent_name: str
    model_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float
    execution_time_seconds: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    success: bool = True
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert metrics to dictionary"""
        return {
            "agent_name": self.agent_name,
            "model_name": self.model_name,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "input_cost_usd": self.input_cost_usd,
            "output_cost_usd": self.output_cost_usd,
            "total_cost_usd": self.total_cost_usd,
            "execution_time_seconds": self.execution_time_seconds,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "error_message": self.error_message,
        }
