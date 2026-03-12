"""
Test script for AIOpsGuard
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiops_guard import AIOpsGuard, get_global_tracker, track_llm_call
import time


# Test 1: Basic decorator usage
@AIOpsGuard(agent_name="TestAgent", model_name="gpt-3.5-turbo")
def test_basic_call(prompt: str) -> str:
    """Test basic LLM call"""
    time.sleep(0.05)
    return "This is a test response to your prompt about AI and machine learning."


# Test 2: Functional decorator
@track_llm_call(agent_name="FunctionalAgent", model_name="gpt-4")
def test_functional_decorator(prompt: str) -> str:
    """Test functional decorator"""
    time.sleep(0.08)
    return "Functional decorator test response with detailed information about the topic."


# Test 3: Different models
@AIOpsGuard(agent_name="ClaudeAgent", model_name="claude-3-sonnet")
def test_claude_call(prompt: str) -> str:
    """Test Claude model"""
    time.sleep(0.06)
    return "Claude response with thoughtful analysis and comprehensive details."


@AIOpsGuard(agent_name="GPT4Agent", model_name="gpt-4-turbo")
def test_gpt4_turbo(prompt: str) -> str:
    """Test GPT-4 Turbo"""
    time.sleep(0.1)
    return "GPT-4 Turbo response with advanced reasoning and detailed explanations about complex topics."


# Test 4: Error handling
@AIOpsGuard(agent_name="ErrorAgent", model_name="gpt-3.5-turbo")
def test_error_handling(prompt: str) -> str:
    """Test error handling"""
    if "error" in prompt.lower():
        raise ValueError("Simulated error in LLM call")
    return "Successful response"


def run_tests():
    """Run all tests"""
    print("🧪 Testing AIOpsGuard\n")
    print("=" * 60)
    
    # Test 1: Basic calls
    print("\n1️⃣  Testing basic decorator...")
    test_basic_call("What is artificial intelligence?")
    test_basic_call("Explain neural networks")
    print("✅ Basic decorator test passed")
    
    # Test 2: Functional decorator
    print("\n2️⃣  Testing functional decorator...")
    test_functional_decorator("Describe deep learning")
    print("✅ Functional decorator test passed")
    
    # Test 3: Different models
    print("\n3️⃣  Testing different models...")
    test_claude_call("Analyze this situation")
    test_gpt4_turbo("Provide detailed analysis")
    print("✅ Different models test passed")
    
    # Test 4: Multiple calls from same agent
    print("\n4️⃣  Testing multiple calls...")
    for i in range(3):
        test_basic_call(f"Question {i+1}: Tell me about AI")
    print("✅ Multiple calls test passed")
    
    # Test 5: Error handling
    print("\n5️⃣  Testing error handling...")
    try:
        test_error_handling("This will cause an error")
    except ValueError:
        print("✅ Error handling test passed (error caught as expected)")
    
    # Test successful call after error
    test_error_handling("This is a normal call")
    
    print("\n" + "=" * 60)
    print("\n📊 Generating Summary Report...\n")
    
    # Get tracker and print summary
    tracker = get_global_tracker()
    tracker.print_summary(show_agents=True, show_models=True)
    
    # Test summary methods
    print("\n" + "=" * 60)
    print("\n🔍 Testing Summary Methods:\n")
    
    summary = tracker.get_summary()
    print(f"Total calls: {summary['total_calls']}")
    print(f"Total cost: ${summary['total_cost_usd']:.4f}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    
    agent_summary = tracker.get_agent_summary()
    print(f"\nTracked agents: {list(agent_summary.keys())}")
    
    model_summary = tracker.get_model_summary()
    print(f"Used models: {list(model_summary.keys())}")
    
    print("\n✅ All tests completed successfully!")


if __name__ == "__main__":
    run_tests()
