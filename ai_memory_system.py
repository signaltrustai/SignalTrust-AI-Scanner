#!/usr/bin/env python3
"""
AI Memory System - Persistent Memory for All AI Agents
Remembers everything: conversations, commands, data, learnings
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger('AIMemory')


class AIMemorySystem:
    """Persistent memory system for AI agents"""
    
    def __init__(self, db_path: str = 'data/ai_memory.db'):
        """Initialize AI Memory System
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info("🧠 AI Memory System initialized")
        logger.info(f"   Database: {db_path}")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table - Everything said to/by AI
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                ai_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Commands table - All commands given by user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                command TEXT NOT NULL,
                parameters TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                executed_at DATETIME,
                error TEXT
            )
        ''')
        
        # Learnings table - Everything AI learns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learning_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                content TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Market data table - All collected market data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                data_type TEXT NOT NULL,
                data TEXT NOT NULL,
                source TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Predictions table - All predictions made
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL,
                actual_outcome TEXT,
                accuracy REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                validated_at DATETIME
            )
        ''')
        
        # User preferences table - Remember user preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, preference_key)
            )
        ''')
        
        # Events table - All important events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT NOT NULL,
                importance TEXT DEFAULT 'normal',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Memory database initialized with 7 tables")
    
    def remember_conversation(self, user_id: str, role: str, content: str, 
                             ai_type: str = None, metadata: Dict = None):
        """Remember a conversation message
        
        Args:
            user_id: User identifier
            role: Message role (user/assistant)
            content: Message content
            ai_type: Type of AI (optional)
            metadata: Additional metadata (optional)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (user_id, role, content, ai_type, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, role, content, ai_type, json.dumps(metadata) if metadata else None))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"💭 Remembered conversation: {role} message from {user_id}")
    
    def remember_command(self, user_id: str, command: str, parameters: Dict = None) -> int:
        """Remember a user command
        
        Args:
            user_id: User identifier
            command: Command text
            parameters: Command parameters (optional)
            
        Returns:
            Command ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO commands (user_id, command, parameters)
            VALUES (?, ?, ?)
        ''', (user_id, command, json.dumps(parameters) if parameters else None))
        
        command_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"📝 Command remembered: '{command}' from {user_id}")
        return command_id
    
    def update_command_status(self, command_id: int, status: str, 
                            result: Any = None, error: str = None):
        """Update command execution status
        
        Args:
            command_id: Command ID
            status: New status (pending/executing/completed/failed)
            result: Execution result (optional)
            error: Error message if failed (optional)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE commands 
            SET status = ?, result = ?, error = ?, 
                executed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, json.dumps(result) if result else None, error, command_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Command {command_id} status updated: {status}")
    
    def remember_learning(self, learning_type: str, subject: str, 
                         content: str, confidence: float = 0.5, 
                         metadata: Dict = None):
        """Remember something learned
        
        Args:
            learning_type: Type of learning (pattern/correlation/trend/etc)
            subject: Subject of learning
            content: Learning content
            confidence: Confidence level (0-1)
            metadata: Additional metadata
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO learnings (learning_type, subject, content, confidence, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (learning_type, subject, content, confidence, 
              json.dumps(metadata) if metadata else None))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🧠 New learning: {learning_type} about {subject} (confidence: {confidence:.0%})")
    
    def remember_market_data(self, symbol: str, data_type: str, 
                           data: Dict, source: str = None):
        """Remember market data
        
        Args:
            symbol: Asset symbol
            data_type: Type of data (price/volume/sentiment/etc)
            data: Data content
            source: Data source
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO market_data (symbol, data_type, data, source)
            VALUES (?, ?, ?, ?)
        ''', (symbol, data_type, json.dumps(data), source))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"📊 Market data remembered: {symbol} - {data_type}")
    
    def remember_prediction(self, symbol: str, prediction: str, 
                          confidence: float = None):
        """Remember a prediction
        
        Args:
            symbol: Asset symbol
            prediction: Prediction content
            confidence: Confidence level
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (symbol, prediction, confidence)
            VALUES (?, ?, ?)
        ''', (symbol, prediction, confidence))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🔮 Prediction remembered: {symbol}")
    
    def remember_preference(self, user_id: str, key: str, value: str):
        """Remember user preference
        
        Args:
            user_id: User identifier
            key: Preference key
            value: Preference value
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, preference_key, preference_value)
            VALUES (?, ?, ?)
        ''', (user_id, key, value))
        
        conn.commit()
        conn.close()
        
        logger.info(f"⚙️  Preference remembered: {user_id} - {key}={value}")
    
    def remember_event(self, event_type: str, event_data: Dict, 
                      importance: str = 'normal'):
        """Remember an event
        
        Args:
            event_type: Type of event
            event_data: Event data
            importance: Event importance (low/normal/high/critical)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (event_type, event_data, importance)
            VALUES (?, ?, ?)
        ''', (event_type, json.dumps(event_data), importance))
        
        conn.commit()
        conn.close()
        
        logger.info(f"📌 Event remembered: {event_type} ({importance})")
    
    def recall_conversations(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Recall conversation history
        
        Args:
            user_id: User identifier
            limit: Maximum messages to recall
            
        Returns:
            List of conversation messages
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, ai_type, timestamp, metadata
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'role': row[0],
                'content': row[1],
                'ai_type': row[2],
                'timestamp': row[3],
                'metadata': json.loads(row[4]) if row[4] else None
            })
        
        conn.close()
        
        return list(reversed(conversations))  # Oldest first
    
    def recall_commands(self, user_id: str = None, status: str = None, 
                       limit: int = 50) -> List[Dict]:
        """Recall commands
        
        Args:
            user_id: Filter by user (optional)
            status: Filter by status (optional)
            limit: Maximum commands to recall
            
        Returns:
            List of commands
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT id, user_id, command, parameters, status, result, timestamp, executed_at, error FROM commands WHERE 1=1'
        params = []
        
        if user_id:
            query += ' AND user_id = ?'
            params.append(user_id)
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        commands = []
        for row in cursor.fetchall():
            commands.append({
                'id': row[0],
                'user_id': row[1],
                'command': row[2],
                'parameters': json.loads(row[3]) if row[3] else None,
                'status': row[4],
                'result': json.loads(row[5]) if row[5] else None,
                'timestamp': row[6],
                'executed_at': row[7],
                'error': row[8]
            })
        
        conn.close()
        
        return commands
    
    def recall_learnings(self, learning_type: str = None, 
                        subject: str = None, limit: int = 100) -> List[Dict]:
        """Recall learnings
        
        Args:
            learning_type: Filter by type (optional)
            subject: Filter by subject (optional)
            limit: Maximum learnings to recall
            
        Returns:
            List of learnings
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT learning_type, subject, content, confidence, timestamp, metadata FROM learnings WHERE 1=1'
        params = []
        
        if learning_type:
            query += ' AND learning_type = ?'
            params.append(learning_type)
        
        if subject:
            query += ' AND subject LIKE ?'
            params.append(f'%{subject}%')
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        learnings = []
        for row in cursor.fetchall():
            learnings.append({
                'type': row[0],
                'subject': row[1],
                'content': row[2],
                'confidence': row[3],
                'timestamp': row[4],
                'metadata': json.loads(row[5]) if row[5] else None
            })
        
        conn.close()
        
        return learnings
    
    def recall_preference(self, user_id: str, key: str) -> Optional[str]:
        """Recall a user preference
        
        Args:
            user_id: User identifier
            key: Preference key
            
        Returns:
            Preference value or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT preference_value
            FROM user_preferences
            WHERE user_id = ? AND preference_key = ?
        ''', (user_id, key))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_memory_stats(self) -> Dict:
        """Get memory system statistics
        
        Returns:
            Statistics dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records in each table
        tables = ['conversations', 'commands', 'learnings', 'market_data', 
                 'predictions', 'user_preferences', 'events']
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            stats[table] = count
        
        # Total memory
        stats['total_memories'] = sum(stats.values())
        
        # Database size
        stats['database_size_kb'] = os.path.getsize(self.db_path) / 1024
        
        conn.close()
        
        return stats
    
    def search_memory(self, query: str, limit: int = 50) -> List[Dict]:
        """Search across all memories
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            Search results from all tables
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        results = []
        
        # Search conversations
        cursor.execute('''
            SELECT 'conversation' as type, content, timestamp
            FROM conversations
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit // 5))
        
        for row in cursor.fetchall():
            results.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        # Search commands
        cursor.execute('''
            SELECT 'command' as type, command, timestamp
            FROM commands
            WHERE command LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit // 5))
        
        for row in cursor.fetchall():
            results.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        # Search learnings
        cursor.execute('''
            SELECT 'learning' as type, content, timestamp
            FROM learnings
            WHERE content LIKE ? OR subject LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit // 5))
        
        for row in cursor.fetchall():
            results.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        
        # Sort by timestamp
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return results[:limit]


# Global memory instance
_memory_instance = None


def get_memory() -> AIMemorySystem:
    """Get or create global memory instance"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = AIMemorySystem()
    return _memory_instance


if __name__ == "__main__":
    # Test memory system
    print("🧠 Testing AI Memory System...")
    
    memory = AIMemorySystem()
    
    # Test conversations
    memory.remember_conversation('test_user', 'user', 'Hello AI!')
    memory.remember_conversation('test_user', 'assistant', 'Hello! How can I help?')
    
    # Test commands
    cmd_id = memory.remember_command('test_user', 'scan markets', {'market': 'crypto'})
    memory.update_command_status(cmd_id, 'completed', {'scanned': 100})
    
    # Test learnings
    memory.remember_learning('pattern', 'BTC', 'Bullish trend detected', 0.85)
    
    # Test preferences
    memory.remember_preference('test_user', 'language', 'french')
    
    # Get stats
    stats = memory.get_memory_stats()
    print("\n📊 Memory Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Memory system test complete!")
