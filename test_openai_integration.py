#!/usr/bin/env python3
"""
Test script for OpenAI integration
Tests the basic functionality of the OpenAI-powered AI system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_configuration():
    """Test if OpenAI is configured"""
    print("Testing OpenAI Configuration...")
    print("-" * 60)
    
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OPENAI_API_KEY not configured")
        print()
        print("To fix this:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Get your API key from: https://platform.openai.com/api-keys")
        print("3. Add it to .env file: OPENAI_API_KEY=sk-proj-your-key-here")
        print()
        return False
    
    print(f"✓ OPENAI_API_KEY is configured")
    print(f"✓ Using model: {model}")
    print(f"✓ API key starts with: {api_key[:15]}...")
    print()
    return True

def test_openai_import():
    """Test if OpenAI library is installed"""
    print("Testing OpenAI Library...")
    print("-" * 60)
    
    try:
        from openai import OpenAI
        print("✓ OpenAI library is installed")
        print()
        return True
    except ImportError:
        print("❌ OpenAI library not installed")
        print()
        print("To fix this:")
        print("  pip install openai")
        print()
        return False

def test_asi1_integration():
    """Test if ASI1 integration module loads"""
    print("Testing ASI1 Integration Module...")
    print("-" * 60)
    
    try:
        from asi1_integration import ASI1AIIntegration
        print("✓ ASI1AIIntegration module loaded successfully")
        print()
        return True
    except Exception as e:
        print(f"❌ Failed to load ASI1AIIntegration: {e}")
        print()
        return False

def test_basic_functionality():
    """Test basic AI functionality"""
    print("Testing Basic AI Functionality...")
    print("-" * 60)
    
    try:
        from asi1_integration import ASI1AIIntegration
        
        # Initialize AI
        ai = ASI1AIIntegration()
        print("✓ AI initialized successfully")
        
        # Test simple market analysis (with minimal data to reduce costs)
        test_data = {
            "symbol": "TEST",
            "price": 100,
            "change_24h": 5.0
        }
        
        print("✓ Running basic analysis test...")
        print("  (This will make a real API call and may take a few seconds)")
        
        result = ai.analyze_market_with_ai(test_data, context="Simple test")
        
        if result.get('success'):
            print("✓ Analysis completed successfully")
            print(f"✓ Provider: {result.get('provider', 'N/A')}")
            print(f"✓ Model: {result.get('model', 'N/A')}")
            print()
            print("Sample response:")
            print(result.get('analysis', '')[:200] + "...")
            print()
            return True
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

def main():
    """Run all tests"""
    print()
    print("=" * 60)
    print("SignalTrust AI Scanner - OpenAI Integration Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Configuration", test_openai_configuration),
        ("OpenAI Library", test_openai_import),
        ("ASI1 Integration", test_asi1_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Only run functionality test if all basic tests pass
    if all(r[1] for r in results):
        print("=" * 60)
        print("All basic tests passed! Running functionality test...")
        print("=" * 60)
        print()
        
        func_result = test_basic_functionality()
        results.append(("Functionality", func_result))
    else:
        print("⚠️ Skipping functionality test due to configuration issues")
        print()
    
    # Print summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    
    if all(r[1] for r in results):
        print("🎉 All tests passed! OpenAI integration is working correctly.")
        print()
        print("Next steps:")
        print("  - Run the full example: python example_openai_usage.py")
        print("  - Start the web application: python start.py")
        print("  - Read the setup guide: cat OPENAI_SETUP_GUIDE.md")
        return 0
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
        print()
        print("For help, see: OPENAI_SETUP_GUIDE.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
