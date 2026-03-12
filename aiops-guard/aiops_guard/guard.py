"""
Main AIOpsGuard decorator and monitoring functionality
"""
import time
import asyncio
import functools
from typing import Callable, Optional, Any, TypeVar, ParamSpec
import tiktoken

from .models import CallMetrics, ModelPricing
from .tracker import CallTracker


# Type variables for generic decorator
P = ParamSpec('P')
R = TypeVar('R')


# Global tracker instance
_global_tracker = CallTracker()


def get_global_tracker() -> CallTracker:
    """Get the global call tracker instance"""
    return _global_tracker


class AIOpsGuard:
    """
    Decorator class for monitoring LLM calls
    
    Usage:
        @AIOpsGuard(agent_name="my_agent", model_name="gpt-4")
        def my_llm_call(prompt: str) -> str:
            # Your LLM call here
            return response
    """
    
    def __init__(
        self,
        agent_name: str,
        model_name: str = "gpt-3.5-turbo",
        tracker: Optional[CallTracker] = None,
        auto_print: bool = False,
    ):
        """
        Initialize the AIOpsGuard decorator
        
        Args:
            agent_name: Name of the agent making the call
            model_name: Name of the LLM model being used
            tracker: Optional custom tracker (uses global tracker if None)
            auto_print: Whether to automatically print summary after each call
        """
        self.agent_name = agent_name
        self.model_name = model_name
        self.tracker = tracker or _global_tracker
        self.auto_print = auto_print
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in a text string
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))
    
    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
    ) -> tuple[float, float, float]:
        """
        Calculate cost for input and output tokens
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Tuple of (input_cost, output_cost, total_cost) in USD
        """
        try:
            input_price, output_price = ModelPricing.get_pricing(self.model_name)
            
            # Convert from per 1M tokens to actual cost
            input_cost = (input_tokens / 1_000_000) * input_price
            output_cost = (output_tokens / 1_000_000) * output_price
            total_cost = input_cost + output_cost
            
            return input_cost, output_cost, total_cost
        except Exception:
            # Return zero cost if calculation fails
            return 0.0, 0.0, 0.0
    
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorator implementation (supports both sync and async functions)
        
        Args:
            func: Function to wrap
            
        Returns:
            Wrapped function
        """
        # Check if function is async
        if asyncio.iscoroutinefunction(func):
            return self._wrap_async(func)
        else:
            return self._wrap_sync(func)
    
    def _wrap_sync(self, func: Callable[P, R]) -> Callable[P, R]:
        """Wrap synchronous function"""
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Extract input text (assumes first arg or 'prompt' kwarg)
            input_text = ""
            if args:
                input_text = str(args[0])
            elif "prompt" in kwargs:
                input_text = str(kwargs["prompt"])
            elif "messages" in kwargs:
                # Handle chat format
                messages = kwargs["messages"]
                if isinstance(messages, list):
                    input_text = " ".join(str(msg) for msg in messages)
                else:
                    input_text = str(messages)
            
            # Count input tokens
            input_tokens = self.count_tokens(input_text)
            
            # Track execution time
            start_time = time.time()
            success = True
            error_message = None
            output_text = ""
            
            try:
                # Execute the function
                result = func(*args, **kwargs)
                output_text = str(result)
                return result
            
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Count output tokens
                output_tokens = self.count_tokens(output_text) if output_text else 0
                total_tokens = input_tokens + output_tokens
                
                # Calculate costs
                input_cost, output_cost, total_cost = self.calculate_cost(
                    input_tokens, output_tokens
                )
                
                # Create metrics
                metrics = CallMetrics(
                    agent_name=self.agent_name,
                    model_name=self.model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=total_tokens,
                    input_cost_usd=input_cost,
                    output_cost_usd=output_cost,
                    total_cost_usd=total_cost,
                    execution_time_seconds=execution_time,
                    success=success,
                    error_message=error_message,
                )
                
                # Track the call
                self.tracker.add_call(metrics)
                
                # Auto-print if enabled
                if self.auto_print:
                    self.tracker.print_summary()
        
        return wrapper


def track_llm_call(
    agent_name: str,
    model_name: str = "gpt-3.5-turbo",
    tracker: Optional[CallTracker] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Functional decorator for tracking LLM calls
    
    Args:
        agent_name: Name of the agent making the call
        model_name: Name of the LLM model being used
        tracker: Optional custom tracker
        
    Returns:
        Decorator function
        
    Usage:
        @track_llm_call(agent_name="my_agent", model_name="gpt-4")
        def my_function(prompt: str) -> str:
            return llm_response
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        guard = AIOpsGuard(
            agent_name=agent_name,
            model_name=model_name,
            tracker=tracker,
        )
        return guard(func)
    
    return decorator

    def _wrap_async(self, func: Callable[P, R]) -> Callable[P, R]:
        """Wrap asynchronous function"""
        @functools.wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Extract input text (assumes first arg or 'prompt' kwarg)
            input_text = ""
            if args:
                input_text = str(args[0])
            elif "prompt" in kwargs:
                input_text = str(kwargs["prompt"])
            elif "messages" in kwargs:
                # Handle chat format
                messages = kwargs["messages"]
                if isinstance(messages, list):
                    input_text = " ".join(str(msg) for msg in messages)
                else:
                    input_text = str(messages)
            
            # Count input tokens
            input_tokens = self.count_tokens(input_text)
            
            # Track execution time
            start_time = time.time()
            success = True
            error_message = None
            output_text = ""
            
            try:
                # Execute the async function
                result = await func(*args, **kwargs)
                output_text = str(result)
                return result
            
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Count output tokens
                output_tokens = self.count_tokens(output_text) if output_text else 0
                total_tokens = input_tokens + output_tokens
                
                # Calculate costs
                input_cost, output_cost, total_cost = self.calculate_cost(
                    input_tokens, output_tokens
                )
                
                # Create metrics
                metrics = CallMetrics(
                    agent_name=self.agent_name,
                    model_name=self.model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=total_tokens,
                    input_cost_usd=input_cost,
                    output_cost_usd=output_cost,
                    total_cost_usd=total_cost,
                    execution_time_seconds=execution_time,
                    success=success,
                    error_message=error_message,
                )
                
                # Track the call
                self.tracker.add_call(metrics)
                
                # Auto-print if enabled
                if self.auto_print:
                    self.tracker.print_summary()
        
        return async_wrapper
