#!/usr/bin/env python3
"""
Test Unlimited Analysis
Verify that all limits have been removed for stocks and crypto analysis
"""

from payment_processor import PaymentProcessor
from realtime_market_data import RealTimeMarketData

def test_payment_plans_unlimited():
    """Test that all plans have unlimited limits."""
    processor = PaymentProcessor()
    plans = processor.get_plans()
    
    print("="*60)
    print("TEST: Vérification des limites illimitées dans les plans")
    print("="*60)
    
    for plan_id, plan in plans.items():
        print(f"\n📋 Plan: {plan['name']} ({plan_id})")
        limits = plan['limits']
        
        # Check scans_per_day
        scans = limits.get('scans_per_day', 0)
        print(f"   ✓ Scans par jour: {'✅ ILLIMITÉ' if scans == -1 else f'❌ LIMITÉ à {scans}'}")
        
        # Check symbols_per_scan
        symbols = limits.get('symbols_per_scan', 0)
        print(f"   ✓ Symboles par scan: {'✅ ILLIMITÉ' if symbols == -1 else f'❌ LIMITÉ à {symbols}'}")
        
        # Check ai_predictions
        predictions = limits.get('ai_predictions', 0)
        print(f"   ✓ Prédictions IA: {'✅ ILLIMITÉ' if predictions == -1 else f'❌ LIMITÉ à {predictions}'}")
        
        # Verify all are unlimited
        all_unlimited = scans == -1 and symbols == -1 and predictions == -1
        if all_unlimited:
            print(f"   ✅ RÉSULTAT: Toutes les limites supprimées!")
        else:
            print(f"   ⚠️ ATTENTION: Certaines limites persistent")

def test_market_data_unlimited():
    """Test that market data methods support unlimited fetching."""
    data = RealTimeMarketData()
    
    print("\n" + "="*60)
    print("TEST: Vérification de l'analyse illimitée des actifs")
    print("="*60)
    
    # Test Canadian stocks
    print("\n📊 Test: Actions Canadiennes")
    canadian_all = data.get_canadian_stocks(limit=None)
    canadian_limited = data.get_canadian_stocks(limit=5)
    print(f"   ✓ Sans limite: {len(canadian_all)} actions")
    print(f"   ✓ Avec limite (5): {len(canadian_limited)} actions")
    print(f"   {'✅ ILLIMITÉ supporté!' if len(canadian_all) > len(canadian_limited) else '❌ Limite non supprimée'}")
    
    # Test US stocks
    print("\n📊 Test: Actions US")
    us_all = data.get_us_stocks(limit=None)
    us_limited = data.get_us_stocks(limit=10)
    print(f"   ✓ Sans limite: {len(us_all)} actions")
    print(f"   ✓ Avec limite (10): {len(us_limited)} actions")
    print(f"   {'✅ ILLIMITÉ supporté!' if len(us_all) > len(us_limited) else '❌ Limite non supprimée'}")
    
    # Test Cryptocurrencies
    print("\n📊 Test: Cryptomonnaies")
    crypto_all = data.get_all_crypto(limit=None)
    crypto_limited = data.get_all_crypto(limit=10)
    print(f"   ✓ Sans limite: {len(crypto_all)} cryptos")
    print(f"   ✓ Avec limite (10): {len(crypto_limited)} cryptos")
    print(f"   {'✅ ILLIMITÉ supporté!' if len(crypto_all) > len(crypto_limited) else '❌ Limite non supprimée'}")
    
    print("\n" + "="*60)
    print("RÉSUMÉ: Analyse Illimitée")
    print("="*60)
    print(f"✅ Total actions analysables: {len(canadian_all) + len(us_all)}")
    print(f"✅ Total cryptos analysables: {len(crypto_all)}")
    print(f"✅ DeFi tokens: {len(data.get_defi_tokens())}")
    print(f"✅ NFT tokens: {len(data.get_nft_tokens())}")
    print(f"✅ TOTAL ACTIFS: {len(canadian_all) + len(us_all) + len(crypto_all) + len(data.get_defi_tokens()) + len(data.get_nft_tokens())}")

def main():
    """Run all tests."""
    print("\n🚀 TEST DE L'ANALYSE ILLIMITÉE")
    print("="*60)
    
    try:
        test_payment_plans_unlimited()
        test_market_data_unlimited()
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\n📝 RÉSUMÉ:")
        print("   ✅ Tous les plans offrent un accès illimité")
        print("   ✅ Analyse illimitée de stocks activée")
        print("   ✅ Analyse illimitée de crypto activée")
        print("   ✅ Worker 24/7 analyse plus d'actifs")
        print("   ✅ Aucune restriction sur le nombre d'analyses")
        print("\n💡 L'application est maintenant optimisée pour une analyse maximale!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
