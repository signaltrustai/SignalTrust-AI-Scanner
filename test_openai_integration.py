#!/usr/bin/env python3
"""
Test script for Groq integration
Tests the basic functionality of the Groq-powered AI system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_configuration():
    """Test if Groq is configured"""
    print("Testing Groq Configuration...")
    print("-" * 60)
    
    api_key = os.getenv('GROQ_API_KEY')
    model = os.getenv('GROQ_MODEL', 'llama3-70b-8192')
    
    if not api_key or api_key == 'your_groq_api_key_here':
        print("❌ GROQ_API_KEY not configured")
        print()
        print("To fix this:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Get your API key from: https://console.groq.com/keys")
        print("3. Add it to .env file: GROQ_API_KEY=gsk_your-key-here")
        print()
        return False
    
    print(f"✓ GROQ_API_KEY is configured")
    print(f"✓ Using model: {model}")
    print(f"✓ API key starts with: {api_key[:15]}...")
    print()
    return True

def test_openai_import():
    """Test if OpenAI library is installed (used for Groq compatibility)"""
    print("Testing OpenAI Library (Groq-compatible)...")
    print("-" * 60)
    
    try:
        from openai import OpenAI
        print("✓ OpenAI library is installed (used for Groq API compatibility)")
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
    """Test if AI integration module loads"""
    print("Testing AI Integration Module...")
    print("-" * 60)
    
    try:
        from asi1_integration import ASI1AIIntegration
        print("✓ AI integration module loaded successfully")
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
    print("SignalTrust AI Scanner - Groq Integration Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Configuration", test_groq_configuration),
        ("OpenAI Library", test_openai_import),
        ("AI Integration", test_asi1_integration),
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
        print("🎉 All tests passed! Groq integration is working correctly.")
        print()
        print("Next steps:")
        print("  - Start the web application: python start.py")
        return 0
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
