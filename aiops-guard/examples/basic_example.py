"""
Basic example of using AIOpsGuard
"""
import time
from aiops_guard import AIOpsGuard, get_global_tracker


# Example 1: Simple function decoration
@AIOpsGuard(agent_name="SimpleAgent", model_name="gpt-3.5-turbo")
def simple_llm_call(prompt: str) -> str:
    """Simulate a simple LLM call"""
    time.sleep(0.1)  # Simulate API call
    return f"Response to: {prompt}. This is a simulated response with some content."


# Example 2: Different model
@AIOpsGuard(agent_name="AdvancedAgent", model_name="gpt-4")
def advanced_llm_call(prompt: str) -> str:
    """Simulate an advanced LLM call"""
    time.sleep(0.2)  # Simulate longer API call
    return f"Advanced response to: {prompt}. This is a more detailed simulated response with additional context and information."


# Example 3: Multiple calls
@AIOpsGuard(agent_name="ResearchAgent", model_name="gpt-4-turbo")
def research_call(query: str) -> str:
    """Simulate a research agent call"""
    time.sleep(0.15)
    return f"Research findings for: {query}. Here are comprehensive research results with data and analysis."


def main():
    """Run examples and print summary"""
    print("🚀 Running AIOpsGuard Examples\n")
    
    # Make various LLM calls
    print("Making LLM calls...")
    
    simple_llm_call("What is Python?")
    simple_llm_call("Explain machine learning")
    
    advanced_llm_call("Write a detailed analysis of AI trends")
    advanced_llm_call("Explain quantum computing")
    
    research_call("Latest developments in LLMs")
    research_call("Best practices for prompt engineering")
    
    print("\n✅ All calls completed!\n")
    
    # Get the global tracker and print summary
    tracker = get_global_tracker()
    tracker.print_summary(show_agents=True, show_models=True)


if __name__ == "__main__":
    main()
