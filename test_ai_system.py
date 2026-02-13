#!/usr/bin/env python3
"""
Test AI Provider System
Verify that the AI provider system is properly configured and working
"""

import os
import sys
from datetime import datetime


def test_ai_provider_import():
    """Test that AI provider module can be imported"""
    print("🧪 Testing AI provider import...")
    try:
        from ai_provider import (
            AIProvider, 
            OpenAIProvider, 
            AnthropicProvider, 
            LocalModelProvider,
            AIProviderFactory,
            EnhancedAIEngine
        )
        print("✅ AI provider module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import AI provider: {e}")
        return False


def test_ai_predictor_import():
    """Test that enhanced AI predictor can be imported"""
    print("\n🧪 Testing AI predictor import...")
    try:
        from ai_predictor import AIPredictor
        print("✅ AI predictor imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import AI predictor: {e}")
        return False


def test_ai_predictor_initialization():
    """Test AI predictor initialization"""
    print("\n🧪 Testing AI predictor initialization...")
    try:
        from ai_predictor import AIPredictor
        
        # Test with AI disabled
        predictor = AIPredictor(use_real_ai=False)
        print(f"✅ AI predictor initialized (use_real_ai=False)")
        print(f"   Version: {predictor.model_version}")
        print(f"   Real AI: {predictor.use_real_ai}")
        
        # Test with AI enabled (may fallback)
        predictor_ai = AIPredictor(use_real_ai=True)
        print(f"✅ AI predictor initialized (use_real_ai=True)")
        print(f"   Real AI Active: {predictor_ai.use_real_ai}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize AI predictor: {e}")
        return False


def test_ai_provider_detection():
    """Test AI provider auto-detection"""
    print("\n🧪 Testing AI provider auto-detection...")
    try:
        from ai_provider import AIProviderFactory
        
        # Check environment variables
        groq_key = os.environ.get('GROQ_API_KEY', '')
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
        ai_provider = os.environ.get('AI_PROVIDER', '')
        
        print(f"   AI_PROVIDER env: {ai_provider if ai_provider else 'Not set'}")
        print(f"   GROQ_API_KEY: {'Configured' if groq_key else 'Not set'}")
        print(f"   ANTHROPIC_API_KEY: {'Configured' if anthropic_key else 'Not set'}")
        
        # Try to create provider
        try:
            provider = AIProviderFactory.create_provider()
            print(f"✅ AI provider auto-detected: {type(provider).__name__}")
        except Exception as e:
            print(f"⚠️  No AI provider configured (this is OK): {e}")
            print(f"   System will use fallback simulations")
        
        return True
    except Exception as e:
        print(f"❌ Failed to test AI provider: {e}")
        return False


def test_prediction_generation():
    """Test prediction generation with fallback"""
    print("\n🧪 Testing prediction generation...")
    try:
        from ai_predictor import AIPredictor
        
        predictor = AIPredictor(use_real_ai=False)
        result = predictor.predict_price('AAPL', days_ahead=3)
        
        print(f"✅ Prediction generated successfully")
        print(f"   Symbol: {result.get('symbol')}")
        print(f"   Model: {result.get('model_used')}")
        print(f"   AI Powered: {result.get('ai_powered', False)}")
        print(f"   Predictions: {len(result.get('predictions', []))} days")
        
        return True
    except Exception as e:
        print(f"❌ Failed to generate prediction: {e}")
        return False


def test_market_intelligence_import():
    """Test market intelligence import"""
    print("\n🧪 Testing market intelligence import...")
    try:
        from ai_market_intelligence import AIMarketIntelligence
        print("✅ Market intelligence imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import market intelligence: {e}")
        return False


def test_chat_system_import():
    """Test chat system import"""
    print("\n🧪 Testing chat system import...")
    try:
        from ai_chat_system import AIChatSystem
        print("✅ Chat system imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import chat system: {e}")
        return False


def test_optional_dependencies():
    """Test optional AI dependencies"""
    print("\n🧪 Testing optional AI dependencies...")
    
    dependencies = {
        'openai': 'OpenAI SDK (used for Groq compatibility)',
        'anthropic': 'Anthropic Claude support',
        'requests': 'Local model support'
    }
    
    for lib, description in dependencies.items():
        try:
            __import__(lib)
            print(f"✅ {lib}: Installed ({description})")
        except ImportError:
            print(f"⚠️  {lib}: Not installed ({description})")
            print(f"   Install with: pip install {lib}")
    
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("SignalTrust AI - Enhanced AI System Test Suite")
    print("=" * 60)
    print(f"Test started: {datetime.now().isoformat()}")
    print()
    
    tests = [
        test_ai_provider_import,
        test_ai_predictor_import,
        test_ai_predictor_initialization,
        test_ai_provider_detection,
        test_prediction_generation,
        test_market_intelligence_import,
        test_chat_system_import,
        test_optional_dependencies
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    print()
    
    if failed == 0:
        print("🎉 All tests passed! AI system is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Configure your AI provider in .env file")
        print("   2. See AI_ENHANCEMENT_GUIDE.md for detailed setup")
        print("   3. Run: python3 start.py to start the application")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("   2. Check AI_ENHANCEMENT_GUIDE.md for configuration help")
        return 1


if __name__ == "__main__":
    sys.exit(main())
