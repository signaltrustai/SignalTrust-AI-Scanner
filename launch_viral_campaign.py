#!/usr/bin/env python3
"""
SignalTrust AI - Viral Marketing Campaign Launcher
==================================================

Script simple pour lancer la campagne marketing virale en un clic.

Usage:
    python launch_viral_campaign.py

Author: SignalTrust AI Team
Date: 2026-02-08
"""

import os
import sys
from datetime import datetime
from viral_marketing_ai_team import ViralMarketingCampaign


def print_banner():
    """Affiche le banner de lancement"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🚀 SignalTrust AI - Viral Marketing Campaign 🚀          ║
║                                                               ║
║           Système de Marketing Automatisé par IA             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_environment():
    """Vérifie que l'environnement est configuré"""
    print("\n🔍 Vérification de l'environnement...")
    
    required_vars = [
        'GROQ_API_KEY',
        'ANTHROPIC_API_KEY'
    ]
    
    optional_vars = [
        'TWITTER_API_KEY',
        'INSTAGRAM_USERNAME',
        'TIKTOK_USERNAME',
        'YOUTUBE_API_KEY',
        'REDDIT_CLIENT_ID',
        'DISCORD_BOT_TOKEN',
        'TELEGRAM_BOT_TOKEN'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print("\n❌ Variables requises manquantes:")
        for var in missing_required:
            print(f"   - {var}")
        print("\n⚠️  Configurez au moins une clé AI (OpenAI ou Anthropic)")
        print("   pour générer du contenu viral.")
        return False
    
    if missing_optional:
        print("\n⚠️  Variables optionnelles manquantes:")
        for var in missing_optional:
            print(f"   - {var}")
        print("\n   La campagne fonctionnera en mode simulation.")
        print("   Configurez les APIs social media pour posting réel.")
    
    print("\n✅ Environnement configuré!")
    return True


def display_campaign_options():
    """Affiche les options de campagne"""
    print("\n" + "="*60)
    print("📋 OPTIONS DE CAMPAGNE")
    print("="*60)
    print("\n1. 🚀 Lancement Express (30 jours)")
    print("   - Calendrier automatique")
    print("   - Toutes plateformes")
    print("   - Optimisation auto")
    print("\n2. ⚙️  Lancement Personnalisé")
    print("   - Choisir durée")
    print("   - Sélectionner plateformes")
    print("   - Configurer budget")
    print("\n3. 📊 Dashboard Analytics")
    print("   - Voir performances")
    print("   - Métriques temps réel")
    print("   - Rapports détaillés")
    print("\n4. 🔧 Configuration")
    print("   - Vérifier APIs")
    print("   - Tester connexions")
    print("   - Valider setup")
    print("\n0. ❌ Quitter")


def launch_express_campaign():
    """Lance une campagne express de 30 jours"""
    print("\n" + "="*60)
    print("🚀 LANCEMENT CAMPAGNE EXPRESS")
    print("="*60)
    
    print("\n📋 Configuration de la campagne:")
    print("   - Durée: 30 jours")
    print("   - Plateformes: 7 (Twitter, TikTok, Instagram, YouTube, Reddit, Discord, Telegram)")
    print("   - Posts: ~120 générés automatiquement")
    print("   - Budget: $50,000")
    print("   - Target: 100K followers, 5K paid users, $250K revenue")
    
    confirm = input("\n✅ Confirmer le lancement? (oui/non): ").lower()
    
    if confirm not in ['oui', 'yes', 'y', 'o']:
        print("\n❌ Lancement annulé")
        return
    
    print("\n⏳ Initialisation de la campagne...")
    campaign = ViralMarketingCampaign()
    
    print("⏳ Génération du contenu viral...")
    result = campaign.launch_campaign(duration_days=30)
    
    print("\n" + "="*60)
    print("✅ CAMPAGNE LANCÉE AVEC SUCCÈS!")
    print("="*60)
    
    print(f"\n📊 Détails du lancement:")
    print(f"   Status: {result['status']}")
    print(f"   Début: {result['campaign_start']}")
    print(f"   Durée: {result['duration']}")
    print(f"   Contenu: {result['content_pieces']} posts")
    print(f"   Plateformes: {', '.join(result['platforms'][:3])}...")
    print(f"   Reach prévu: {result['estimated_reach']}")
    print(f"   Revenue target: {result['target_revenue']}")
    print(f"   ROI prévu: {result['expected_roi']}")
    
    print(f"\n🤖 Équipe d'IA:")
    for agent, status in result['team'].items():
        print(f"   {agent}: {status}")
    
    print(f"\n📋 Prochaines étapes:")
    for step in result['next_steps']:
        print(f"   {step}")
    
    print("\n💡 La campagne est maintenant active!")
    print("   Utilisez l'option 3 (Dashboard) pour suivre les performances")
    
    return campaign


def launch_custom_campaign():
    """Lance une campagne personnalisée"""
    print("\n" + "="*60)
    print("⚙️  LANCEMENT CAMPAGNE PERSONNALISÉE")
    print("="*60)
    
    # Durée
    while True:
        try:
            days = input("\n📅 Durée de la campagne (jours, default 30): ")
            days = int(days) if days else 30
            if days > 0:
                break
            print("   ⚠️  La durée doit être > 0")
        except ValueError:
            print("   ⚠️  Veuillez entrer un nombre valide")
    
    # Plateformes
    print("\n📱 Sélection des plateformes:")
    all_platforms = [
        'Twitter/X', 'TikTok', 'Instagram', 'YouTube', 
        'Reddit', 'Discord', 'Telegram'
    ]
    print("   1. Toutes les plateformes (recommandé)")
    print("   2. Sélection manuelle")
    
    platform_choice = input("\n   Choix (1/2): ")
    
    if platform_choice == '2':
        print("\n   Sélectionnez les plateformes (séparées par des virgules):")
        for i, platform in enumerate(all_platforms, 1):
            print(f"   {i}. {platform}")
        selected = input("\n   Numéros (ex: 1,2,3): ")
        # Logique de sélection ici
    
    # Budget
    print("\n💰 Budget:")
    budget_presets = {
        '1': ('Starter', 10000),
        '2': ('Standard', 50000),
        '3': ('Premium', 100000),
        '4': ('Custom', None)
    }
    
    print("   1. Starter ($10K)")
    print("   2. Standard ($50K) - Recommandé")
    print("   3. Premium ($100K)")
    print("   4. Custom")
    
    budget_choice = input("\n   Choix (1-4): ")
    
    if budget_choice == '4':
        while True:
            try:
                budget = int(input("   Budget custom ($): "))
                if budget > 0:
                    break
            except ValueError:
                print("   ⚠️  Veuillez entrer un montant valide")
    else:
        budget = budget_presets.get(budget_choice, ('Standard', 50000))[1]
    
    # Résumé
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DE LA CONFIGURATION")
    print("="*60)
    print(f"\n   Durée: {days} jours")
    print(f"   Plateformes: {len(all_platforms)} sélectionnées")
    print(f"   Budget: ${budget:,}")
    print(f"   Posts prévus: ~{days * 4} posts")
    
    confirm = input("\n✅ Confirmer le lancement? (oui/non): ").lower()
    
    if confirm not in ['oui', 'yes', 'y', 'o']:
        print("\n❌ Lancement annulé")
        return
    
    print("\n⏳ Lancement de la campagne personnalisée...")
    campaign = ViralMarketingCampaign()
    result = campaign.launch_campaign(duration_days=days)
    
    print("\n✅ Campagne personnalisée lancée!")
    return campaign


def show_dashboard(campaign):
    """Affiche le dashboard analytics"""
    if not campaign:
        print("\n❌ Aucune campagne active")
        print("   Lancez d'abord une campagne (options 1 ou 2)")
        return
    
    print("\n" + "="*60)
    print("📊 DASHBOARD ANALYTICS - TEMPS RÉEL")
    print("="*60)
    
    status = campaign.get_campaign_status()
    
    if status.get('campaign_status') == 'inactive':
        print("\n⚠️  Campagne inactive")
        return
    
    # Dashboard en temps réel
    dashboard = status.get('dashboard', {})
    live = dashboard.get('live_metrics', {})
    
    print(f"\n🎯 MÉTRIQUES EN DIRECT")
    print(f"   📅 Jours actifs: {status.get('days_running', 0)}")
    print(f"   👥 Followers: {live.get('current_followers', 0):,}")
    print(f"   📈 Croissance aujourd'hui: +{live.get('followers_growth_today', 0):,}")
    print(f"   👁️  Impressions (1h): {live.get('impressions_last_hour', 0):,}")
    print(f"   💬 Engagement (1h): {live.get('engagement_last_hour', 0):,}")
    print(f"   💰 Revenue aujourd'hui: ${live.get('revenue_today', 0):,}")
    print(f"   ✅ Conversions aujourd'hui: {live.get('conversions_today', 0)}")
    
    # Alertes
    alerts = dashboard.get('alerts', [])
    if alerts:
        print(f"\n🔔 ALERTES RÉCENTES:")
        for alert in alerts:
            icon = {'success': '✅', 'warning': '⚠️', 'opportunity': '💡'}.get(alert['type'], '📌')
            print(f"   {icon} {alert['message']}")
    
    # Top performers
    top = dashboard.get('top_performers_today', [])
    if top:
        print(f"\n🏆 TOP PERFORMERS AUJOURD'HUI:")
        for i, performer in enumerate(top[:3], 1):
            print(f"   {i}. {performer}")
    
    # Performance rapport
    performance = status.get('performance', {})
    overall = performance.get('overall_performance', {})
    
    print(f"\n📈 PERFORMANCE GLOBALE")
    print(f"   Impressions totales: {overall.get('total_impressions', 0):,}")
    print(f"   Reach total: {overall.get('total_reach', 0):,}")
    print(f"   Engagement total: {overall.get('total_engagement', 0):,}")
    print(f"   Conversions: {overall.get('total_conversions', 0):,}")
    print(f"   Revenue: ${overall.get('total_revenue', 0):,}")
    print(f"   ROI: {overall.get('roi', 0)}x")
    print(f"   CAC: ${overall.get('cac', 0):.2f}")
    print(f"   LTV: ${overall.get('ltv', 0):.2f}")
    
    # Breakdown par plateforme
    platforms = performance.get('platform_breakdown', {})
    if platforms:
        print(f"\n📱 BREAKDOWN PAR PLATEFORME:")
        for platform, data in list(platforms.items())[:5]:
            print(f"\n   {platform.title()}:")
            if isinstance(data, dict):
                for key, value in list(data.items())[:3]:
                    if key != 'top_posts' and key != 'top_reels':
                        print(f"      {key}: {value}")
    
    # Insights
    insights = performance.get('insights', [])
    if insights:
        print(f"\n💡 INSIGHTS CLÉS:")
        for insight in insights[:5]:
            print(f"   • {insight}")
    
    # Recommandations
    recommendations = performance.get('recommendations', [])
    if recommendations:
        print(f"\n✨ RECOMMANDATIONS:")
        for rec in recommendations[:5]:
            print(f"   → {rec}")
    
    print("\n" + "="*60)


def show_configuration():
    """Affiche la configuration actuelle"""
    print("\n" + "="*60)
    print("🔧 CONFIGURATION ACTUELLE")
    print("="*60)
    
    # AI Providers
    print("\n🤖 AI Providers:")
    print(f"   Groq: {'✅ Configuré' if os.getenv('GROQ_API_KEY') else '❌ Non configuré'}")
    print(f"   Anthropic: {'✅ Configuré' if os.getenv('ANTHROPIC_API_KEY') else '❌ Non configuré'}")
    
    # Social Media
    print("\n📱 Plateformes Social Media:")
    platforms_status = {
        'Twitter/X': os.getenv('TWITTER_API_KEY'),
        'Instagram': os.getenv('INSTAGRAM_USERNAME'),
        'TikTok': os.getenv('TIKTOK_USERNAME'),
        'YouTube': os.getenv('YOUTUBE_API_KEY'),
        'Reddit': os.getenv('REDDIT_CLIENT_ID'),
        'Discord': os.getenv('DISCORD_BOT_TOKEN'),
        'Telegram': os.getenv('TELEGRAM_BOT_TOKEN')
    }
    
    for platform, configured in platforms_status.items():
        status = '✅ Configuré' if configured else '❌ Non configuré'
        mode = ' (Réel)' if configured else ' (Simulation)'
        print(f"   {platform}: {status}{mode}")
    
    # Analytics
    print("\n📊 Analytics:")
    analytics = {
        'Google Analytics': os.getenv('GA4_MEASUREMENT_ID'),
        'Facebook Pixel': os.getenv('FACEBOOK_PIXEL_ID'),
        'Mixpanel': os.getenv('MIXPANEL_TOKEN')
    }
    
    for tool, configured in analytics.items():
        status = '✅ Configuré' if configured else '❌ Non configuré'
        print(f"   {tool}: {status}")
    
    # Paid Ads
    print("\n💰 Publicité Payante:")
    ads = {
        'Meta Ads': os.getenv('META_ADS_ACCOUNT_ID'),
        'Google Ads': os.getenv('GOOGLE_ADS_CUSTOMER_ID'),
        'TikTok Ads': os.getenv('TIKTOK_ADS_ACCESS_TOKEN')
    }
    
    for platform, configured in ads.items():
        status = '✅ Configuré' if configured else '❌ Non configuré'
        print(f"   {platform}: {status}")
    
    print("\n" + "="*60)
    print("\n💡 Pour configurer:")
    print("   1. Copiez .env.example vers .env")
    print("   2. Remplissez vos API keys")
    print("   3. Relancez ce script")
    print("\n   Minimum requis: OpenAI ou Anthropic API key")


def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifier l'environnement
    if not check_environment():
        print("\n❌ Configuration incomplète. Quitter...")
        sys.exit(1)
    
    campaign = None
    
    while True:
        display_campaign_options()
        
        try:
            choice = input("\n👉 Votre choix (0-4): ").strip()
            
            if choice == '0':
                print("\n👋 Au revoir! Bonne campagne virale! 🚀")
                break
            
            elif choice == '1':
                campaign = launch_express_campaign()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choice == '2':
                campaign = launch_custom_campaign()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choice == '3':
                show_dashboard(campaign)
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choice == '4':
                show_configuration()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            else:
                print("\n❌ Choix invalide. Essayez encore.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interruption détectée. Au revoir!")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            input("\n⏸️  Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
