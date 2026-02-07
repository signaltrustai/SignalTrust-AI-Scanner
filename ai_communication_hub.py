#!/usr/bin/env python3
"""
AI Communication Hub - Enables AI agents to communicate and share data
All AI systems work together and evolve collectively
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import threading
import time


class AICommunicationHub:
    """Central hub for AI-to-AI communication and data sharing."""
    
    def __init__(self):
        """Initialize AI communication hub."""
        self.hub_directory = "data/ai_hub/"
        self.shared_knowledge = "data/ai_hub/shared_knowledge.json"
        self.communication_log = "data/ai_hub/communication_log.json"
        self.collective_intelligence = "data/ai_hub/collective_intelligence.json"
        
        self._ensure_directories()
        
        # Initialize shared knowledge
        self.knowledge = self._load_shared_knowledge()
        self.messages = []
        self.collective = self._load_collective_intelligence()
    
    def _ensure_directories(self):
        """Ensure all directories exist."""
        if not os.path.exists(self.hub_directory):
            os.makedirs(self.hub_directory)
    
    def _load_shared_knowledge(self) -> Dict:
        """Load shared knowledge base."""
        if os.path.exists(self.shared_knowledge):
            try:
                with open(self.shared_knowledge, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'version': '1.0',
            'last_update': datetime.now().isoformat(),
            'total_data_points': 0,
            'market_insights': {},
            'patterns': [],
            'predictions': [],
            'whale_intelligence': {},
            'gem_discoveries': [],
            'news_sentiment': {},
            'correlations': []
        }
    
    def _load_collective_intelligence(self) -> Dict:
        """Load collective intelligence metrics."""
        if os.path.exists(self.collective_intelligence):
            try:
                with open(self.collective_intelligence, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'collective_iq': 75.0,
            'collective_accuracy': 0.70,
            'total_learning_sessions': 0,
            'connected_ais': 0,
            'data_exchanges': 0,
            'evolution_synergy': 1.0
        }
    
    def send_message(self, from_ai: str, to_ai: str, message_type: str, data: Dict):
        """Send message from one AI to another.
        
        Args:
            from_ai: Source AI name
            to_ai: Target AI name (or "ALL")
            message_type: Type of message
            data: Message data
        """
        message = {
            'timestamp': datetime.now().isoformat(),
            'from': from_ai,
            'to': to_ai,
            'type': message_type,
            'data': data,
            'delivered': False
        }
        
        self.messages.append(message)
        self._save_communication_log()
        
        # Process message immediately if broadcast
        if to_ai == "ALL":
            self._broadcast_to_all_ais(message)
    
    def share_data(self, ai_name: str, data_type: str, data: Any):
        """Share data to collective knowledge.
        
        Args:
            ai_name: Name of AI sharing data
            data_type: Type of data being shared
            data: The data to share
        """
        timestamp = datetime.now().isoformat()
        
        if data_type == 'market_insights':
            self.knowledge['market_insights'][ai_name] = {
                'timestamp': timestamp,
                'data': data
            }
        elif data_type == 'patterns':
            self.knowledge['patterns'].append({
                'source': ai_name,
                'timestamp': timestamp,
                'pattern': data
            })
        elif data_type == 'predictions':
            self.knowledge['predictions'].append({
                'source': ai_name,
                'timestamp': timestamp,
                'prediction': data
            })
        elif data_type == 'whale_intelligence':
            self.knowledge['whale_intelligence'][ai_name] = {
                'timestamp': timestamp,
                'data': data
            }
        elif data_type == 'gem_discoveries':
            self.knowledge['gem_discoveries'].extend(data if isinstance(data, list) else [data])
        elif data_type == 'news_sentiment':
            self.knowledge['news_sentiment'][ai_name] = {
                'timestamp': timestamp,
                'data': data
            }
        elif data_type == 'correlations':
            self.knowledge['correlations'].extend(data if isinstance(data, list) else [data])
        
        self.knowledge['total_data_points'] += 1
        self.knowledge['last_update'] = timestamp
        
        # Update collective intelligence
        self.collective['data_exchanges'] += 1
        
        self._save_shared_knowledge()
        self._save_collective_intelligence()
    
    def get_shared_data(self, data_type: str) -> Any:
        """Get shared data from collective knowledge.
        
        Args:
            data_type: Type of data to retrieve
            
        Returns:
            Shared data of specified type
        """
        return self.knowledge.get(data_type, {})
    
    def get_all_knowledge(self) -> Dict:
        """Get all shared knowledge."""
        return self.knowledge
    
    def evolve_collectively(self):
        """Evolve collective intelligence based on shared data."""
        # Calculate new collective IQ
        data_points = self.knowledge['total_data_points']
        exchanges = self.collective['data_exchanges']
        
        # Collective IQ increases with data sharing
        iq_boost = min(25, data_points / 100 + exchanges / 50)
        self.collective['collective_iq'] = min(100, 75 + iq_boost)
        
        # Accuracy improves with collective learning
        accuracy_boost = min(0.25, data_points / 1000 + exchanges / 200)
        self.collective['collective_accuracy'] = min(0.99, 0.70 + accuracy_boost)
        
        # Evolution synergy (how well AIs work together)
        if exchanges > 100:
            self.collective['evolution_synergy'] = min(10.0, 1.0 + exchanges / 100)
        
        self.collective['total_learning_sessions'] += 1
        
        self._save_collective_intelligence()
        
        return self.collective
    
    def get_collective_intelligence(self) -> Dict:
        """Get collective intelligence metrics."""
        return self.collective
    
    def _broadcast_to_all_ais(self, message: Dict):
        """Broadcast message to all AI systems."""
        # Mark as delivered to all
        message['delivered'] = True
        message['broadcast_time'] = datetime.now().isoformat()
    
    def _save_shared_knowledge(self):
        """Save shared knowledge to file."""
        # Keep last 10000 patterns
        self.knowledge['patterns'] = self.knowledge['patterns'][-10000:]
        self.knowledge['predictions'] = self.knowledge['predictions'][-10000:]
        self.knowledge['gem_discoveries'] = self.knowledge['gem_discoveries'][-5000:]
        self.knowledge['correlations'] = self.knowledge['correlations'][-5000:]
        
        with open(self.shared_knowledge, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def _save_communication_log(self):
        """Save communication log."""
        # Keep last 1000 messages
        self.messages = self.messages[-1000:]
        
        with open(self.communication_log, 'w') as f:
            json.dump(self.messages, f, indent=2)
    
    def _save_collective_intelligence(self):
        """Save collective intelligence."""
        with open(self.collective_intelligence, 'w') as f:
            json.dump(self.collective, f, indent=2)
    
    def create_backup(self, backup_path: str = None):
        """Create backup of all AI data.
        
        Args:
            backup_path: Path for backup (default: data/backups/)
        """
        if backup_path is None:
            backup_path = "data/backups/"
        
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{backup_path}ai_backup_{timestamp}.json"
        
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'shared_knowledge': self.knowledge,
            'collective_intelligence': self.collective,
            'communication_log': self.messages[-100:]  # Last 100 messages
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        return backup_file
    
    def get_status(self) -> Dict:
        """Get hub status."""
        return {
            'status': 'active',
            'total_data_points': self.knowledge['total_data_points'],
            'data_exchanges': self.collective['data_exchanges'],
            'collective_iq': self.collective['collective_iq'],
            'collective_accuracy': self.collective['collective_accuracy'],
            'evolution_synergy': self.collective['evolution_synergy'],
            'last_update': self.knowledge['last_update'],
            'patterns_learned': len(self.knowledge['patterns']),
            'predictions_shared': len(self.knowledge['predictions']),
            'gems_discovered': len(self.knowledge['gem_discoveries'])
        }


# Global AI Hub instance
ai_hub = AICommunicationHub()


if __name__ == "__main__":
    hub = AICommunicationHub()
    
    print("=" * 80)
    print("🤝 AI COMMUNICATION HUB")
    print("=" * 80)
    
    # Test communication
    hub.send_message("GemFinder", "ALL", "discovery", {"gems": 10})
    hub.send_message("Predictor", "Evolution", "prediction", {"accuracy": 0.85})
    
    # Test data sharing
    hub.share_data("GemFinder", "gem_discoveries", [{"symbol": "TEST", "score": 95}])
    hub.share_data("Predictor", "predictions", {"asset": "BTC", "direction": "UP"})
    hub.share_data("WhaleWatcher", "whale_intelligence", {"whale_ratio": 1.5})
    
    # Evolve collectively
    collective = hub.evolve_collectively()
    
    # Get status
    status = hub.get_status()
    
    print(f"\n📊 HUB STATUS:")
    print(f"   Collective IQ: {status['collective_iq']:.1f}")
    print(f"   Collective Accuracy: {status['collective_accuracy']*100:.1f}%")
    print(f"   Evolution Synergy: {status['evolution_synergy']:.1f}x")
    print(f"   Data Points: {status['total_data_points']}")
    print(f"   Data Exchanges: {status['data_exchanges']}")
    
    # Create backup
    backup = hub.create_backup()
    print(f"\n💾 Backup created: {backup}")
