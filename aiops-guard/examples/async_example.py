"""
Example: Async function support with AIOpsGuard
"""
import asyncio
from aiops_guard import AIOpsGuard, get_global_tracker


# Simulate async LLM call
@AIOpsGuard(agent_name="AsyncAgent", model_name="gpt-4")
async def async_llm_call(prompt: str) -> str:
    """Simulated async LLM call"""
    await asyncio.sleep(0.1)  # Simulate API latency
    return f"Response to: {prompt}"


# Multiple async agents
@AIOpsGuard(agent_name="FastAgent", model_name="gpt-3.5-turbo")
async def fast_agent(query: str) -> str:
    await asyncio.sleep(0.05)
    return f"Fast response: {query}"


@AIOpsGuard(agent_name="SlowAgent", model_name="gpt-4-turbo")
async def slow_agent(query: str) -> str:
    await asyncio.sleep(0.2)
    return f"Detailed response: {query}"


async def main():
    """Run async examples"""
    print("🚀 Running async LLM calls...\n")
    
    # Single async call
    result1 = await async_llm_call("What is the meaning of life?")
    print(f"Result 1: {result1}\n")
    
    # Concurrent async calls
    tasks = [
        fast_agent("Quick question 1"),
        fast_agent("Quick question 2"),
        slow_agent("Complex analysis needed"),
    ]
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results, 1):
        print(f"Result {i+1}: {result}")
    
    print("\n" + "="*70 + "\n")
    
    # Print summary
    tracker = get_global_tracker()
    tracker.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
