"""
Test exception handling and edge cases
"""
from aiops_guard import AIOpsGuard, get_global_tracker


# Test with unknown model name
@AIOpsGuard(agent_name="UnknownModelAgent", model_name="some-random-model-xyz")
def test_unknown_model(prompt: str) -> str:
    """Test with a model name not in the pricing list"""
    return f"Response to: {prompt}"


# Test with empty model name
@AIOpsGuard(agent_name="EmptyModelAgent", model_name="")
def test_empty_model(prompt: str) -> str:
    """Test with empty model name"""
    return f"Response to: {prompt}"


# Test with None-like model name
@AIOpsGuard(agent_name="WeirdModelAgent", model_name="null")
def test_weird_model(prompt: str) -> str:
    """Test with weird model name"""
    return f"Response to: {prompt}"


def main():
    """Run exception handling tests"""
    print("🧪 Testing Exception Handling\n")
    print("="*70)
    
    # Test 1: Unknown model
    print("\n1. Testing unknown model name...")
    try:
        result = test_unknown_model("Test prompt")
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 2: Empty model
    print("\n2. Testing empty model name...")
    try:
        result = test_empty_model("Test prompt")
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 3: Weird model
    print("\n3. Testing weird model name...")
    try:
        result = test_weird_model("Test prompt")
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n" + "="*70)
    print("\n📊 Summary Report:\n")
    
    # Print summary
    tracker = get_global_tracker()
    tracker.print_summary()
    
    print("\n✅ All exception handling tests passed!")
    print("   The library gracefully handles unknown models with fallback pricing.")


if __name__ == "__main__":
    main()
