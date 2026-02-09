# 🔐 Guide Rapide: Gestion Sécurisée des Clés API

Ce guide explique comment utiliser le nouveau système de gestion sécurisée des clés API.

## 🎯 Qu'est-ce que c'est?

Un système intelligent pour stocker et gérer vos clés API de manière sécurisée avec:

- ✅ **Chiffrement**: Clés chiffrées sur disque (AES-128)
- ✅ **Validation**: Vérification automatique du format
- ✅ **Fallback**: Utilise les variables d'environnement si besoin
- ✅ **Multi-Provider**: Supporte OpenAI, Anthropic, CoinGecko, etc.

## 🚀 Démarrage Rapide

### 1. Configuration du Mot de Passe Maître

Ajoutez à votre fichier `.env`:
```bash
API_MASTER_PASSWORD=votre-mot-de-passe-securise
```

Ou générez-en un:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Stocker vos Clés API

```python
from config.api_keys import KeyManager

# Initialiser le gestionnaire
manager = KeyManager()

# Stocker une clé
manager.set_key('OPENAI_API_KEY', 'sk-proj-...', save=True)
manager.set_key('COINGECKO_API_KEY', 'CG-...', save=True)

# Importer depuis les variables d'environnement
manager.import_from_env()
```

### 3. Récupérer vos Clés

```python
# Récupérer une clé
api_key = manager.get_key('OPENAI_API_KEY')

# Récupérer toutes les clés de données de marché
from config.api_keys.key_manager import get_market_data_keys
keys = get_market_data_keys()
```

### 4. Valider vos Clés

```python
from config.api_keys import KeyValidator

validator = KeyValidator()

# Valider le format
result = validator.validate_key('OPENAI_API_KEY', api_key, test_connection=False)
print(f"Valide: {result['format_valid']}")

# Tester la connexion
result = validator.validate_key('OPENAI_API_KEY', api_key, test_connection=True)
print(f"Connexion OK: {result['connection_valid']}")
```

## 📊 Exemples d'Utilisation

### Rotation de Clés

```python
manager = KeyManager()

# Remplacer une clé existante
manager.rotate_key('OPENAI_API_KEY', 'nouvelle-cle')
```

### Lister les Clés Disponibles

```python
manager = KeyManager()

# Afficher toutes les clés (masquées)
for key_name in manager.list_keys():
    value = manager.get_key(key_name)
    masked = value[:8] + "..." + value[-4:] if value else "N/A"
    print(f"{key_name}: {masked}")
```

### Supprimer une Clé

```python
manager = KeyManager()
manager.delete_key('OLD_API_KEY', save=True)
```

## 🔧 Outils en Ligne de Commande

### Afficher les Clés Stockées

```bash
python3 config/api_keys/key_manager.py
```

### Valider les Clés

```bash
python3 config/api_keys/key_validator.py
```

### Tester le Système

```bash
python3 test_api_key_system.py
```

## 🌐 Utilisation avec Google Colab

Le notebook Colab intègre automatiquement le gestionnaire de clés:

1. Ouvrir le notebook: `SignalTrust_AI_Scanner.ipynb`
2. Exécuter les cellules dans l'ordre
3. Entrer vos clés API quand demandé
4. Les clés sont automatiquement chiffrées et stockées

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/signaltrustai/SignalTrust-AI-Scanner/blob/main/SignalTrust_AI_Scanner.ipynb)

## 🔒 Sécurité

### Bonnes Pratiques

1. ✅ Ne JAMAIS commiter le fichier `keys.enc`
2. ✅ Utiliser un mot de passe maître fort
3. ✅ Changer les clés tous les 90 jours
4. ✅ Utiliser des clés différentes dev/prod
5. ✅ Garder le mot de passe dans un gestionnaire sécurisé

### Fichiers à Protéger

- ❌ `config/api_keys/keys.enc` - JAMAIS dans git
- ❌ `.env` - JAMAIS dans git
- ✅ `.env.example` - OK pour git (valeurs exemple)

## 📚 Documentation Complète

- [config/api_keys/README.md](config/api_keys/README.md) - Documentation technique
- [COPILOT_COLAB_LINK_ENHANCED.md](COPILOT_COLAB_LINK_ENHANCED.md) - Guide Colab
- [.env.example](.env.example) - Configuration exemple

## 🐛 Dépannage

### Erreur: "No cipher initialized"

**Solution**: Définir `API_MASTER_PASSWORD` dans `.env`

### Erreur: "Key format invalid"

**Solution**: Vérifier le format de votre clé API chez le fournisseur

### Erreur: "Connection timeout"

**Solution**: Vérifier votre connexion internet et le statut de l'API

## 🎯 Providers Supportés

### IA / AI
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic (Claude)
- ✅ Local (Ollama)

### Données de Marché
- ✅ CoinGecko (Crypto)
- ✅ Alpha Vantage (Actions)
- ✅ Whale Alert (Transactions blockchain)
- ✅ NewsCatcher (Actualités)

## 💡 Conseils

1. **Première utilisation**: Importer vos clés depuis `.env`
   ```python
   manager = KeyManager()
   manager.import_from_env()
   ```

2. **Test régulier**: Valider vos clés régulièrement
   ```bash
   python3 test_api_key_system.py
   ```

3. **Backup**: Sauvegarder `keys.enc` de manière sécurisée

## 🤝 Support

- 📖 Documentation: Voir les fichiers README
- 🐛 Bugs: [GitHub Issues](https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues)
- 💬 Questions: [GitHub Discussions](https://github.com/signaltrustai/SignalTrust-AI-Scanner/discussions)

---

**Fait avec 🔒 par SignalTrust AI**

✨ **Vos clés API sont maintenant en sécurité!**
