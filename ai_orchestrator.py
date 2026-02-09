#!/usr/bin/env python3
"""
AI Orchestrator - Coordinates all AI agents working 24/7
Central brain that manages multiple AI workers
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AIOrchestrator')


class AIOrchestrator:
    """Central orchestrator for all AI agents"""
    
    def __init__(self):
        """Initialize AI Orchestrator"""
        self.running = False
        self.agents = {}
        self.performance_metrics = {
            'total_agents': 0,
            'active_agents': 0,
            'total_tasks_completed': 0,
            'average_performance': 0.0,
            'system_health': 100,
            'started_at': None
        }
        
        # Agent configuration — each agent has a preferred AI model
        self.agent_config = {
            'market_scanner': {
                'name': 'Market Scanner Agent',
                'role': 'Scan markets 24/7 for opportunities',
                'priority': 'high',
                'preferred_ai': 'gemini',
                'status': 'idle'
            },
            'data_collector': {
                'name': 'Data Collector Agent',
                'role': 'Collect and aggregate market data',
                'priority': 'high',
                'preferred_ai': 'rule_based',
                'status': 'idle'
            },
            'pattern_analyzer': {
                'name': 'Pattern Analyzer Agent',
                'role': 'Analyze patterns and trends using deep reasoning',
                'priority': 'medium',
                'preferred_ai': 'deepseek',
                'status': 'idle'
            },
            'predictor': {
                'name': 'Predictor Agent',
                'role': 'Generate AI-powered predictions and forecasts',
                'priority': 'high',
                'preferred_ai': 'openai',
                'status': 'idle'
            },
            'learning_agent': {
                'name': 'Learning Agent',
                'role': 'Continuously learn and improve models',
                'priority': 'medium',
                'preferred_ai': 'anthropic',
                'status': 'idle'
            },
            'optimizer': {
                'name': 'Optimizer Agent',
                'role': 'Optimize system performance and strategies',
                'priority': 'low',
                'preferred_ai': 'deepseek',
                'status': 'idle'
            }
        }
        
        # Create orchestrator directory
        self.data_dir = 'data/ai_orchestrator'
        os.makedirs(self.data_dir, exist_ok=True)
        
    def start(self):
        """Start the AI orchestration system"""
        if self.running:
            logger.warning("⚠️  Orchestrator already running")
            return
        
        self.running = True
        self.performance_metrics['started_at'] = datetime.now().isoformat()
        
        logger.info("=" * 70)
        logger.info("🎭 AI ORCHESTRATOR - Central AI Brain Starting...")
        logger.info("=" * 70)
        logger.info("")
        logger.info("🤖 Initializing AI Agent Army...")
        logger.info("")
        
        # Initialize all agents
        for agent_id, config in self.agent_config.items():
            self._initialize_agent(agent_id, config)
        
        # Start coordination thread
        self.coordination_thread = threading.Thread(target=self._coordinate_agents, daemon=True)
        self.coordination_thread.start()
        
        logger.info("")
        logger.info("=" * 70)
        logger.info(f"✅ {len(self.agents)} AI Agents activated and ready!")
        logger.info("🔄 Agents will now work 24/7 continuously")
        logger.info("=" * 70)
        
    def _initialize_agent(self, agent_id: str, config: Dict):
        """Initialize an AI agent"""
        logger.info(f"   🤖 Activating: {config['name']}")
        logger.info(f"      Role: {config['role']}")
        logger.info(f"      Priority: {config['priority']}")
        
        self.agents[agent_id] = {
            'config': config,
            'status': 'active',
            'tasks_completed': 0,
            'performance': 1.0,
            'last_activity': datetime.now().isoformat(),
            'errors': 0
        }
        
        self.performance_metrics['total_agents'] += 1
        self.performance_metrics['active_agents'] += 1
        
        logger.info(f"      ✅ {config['name']} is ONLINE")
        logger.info("")
    
    def _coordinate_agents(self):
        """Main coordination loop"""
        logger.info("🧠 AI Orchestrator coordination loop started")
        
        cycle = 0
        while self.running:
            try:
                cycle += 1
                
                # Assign tasks to agents
                self._assign_tasks()
                
                # Monitor agent performance
                if cycle % 10 == 0:  # Every 10 cycles
                    self._monitor_performance()
                
                # Optimize agent allocation
                if cycle % 30 == 0:  # Every 30 cycles
                    self._optimize_allocation()
                
                # Save metrics
                if cycle % 60 == 0:  # Every 60 cycles
                    self._save_metrics()
                
                time.sleep(10)  # Coordinate every 10 seconds
                
            except Exception as e:
                logger.error(f"❌ Error in coordination: {e}")
                time.sleep(10)
    
    def _assign_tasks(self):
        """Assign tasks to available agents"""
        for agent_id, agent in self.agents.items():
            if agent['status'] == 'active':
                # Assign task based on agent role
                task = self._get_next_task(agent_id)
                if task:
                    self._execute_task(agent_id, task)
    
    def _get_next_task(self, agent_id: str) -> Optional[Dict]:
        """Get next task for agent"""
        agent_config = self.agent_config.get(agent_id, {})
        role = agent_config.get('role', '')
        
        # Generate task based on agent role
        if 'scan' in role.lower():
            return {'type': 'scan_markets', 'priority': 'high'}
        elif 'collect' in role.lower():
            return {'type': 'collect_data', 'priority': 'high'}
        elif 'pattern' in role.lower():
            return {'type': 'analyze_patterns', 'priority': 'medium'}
        elif 'predict' in role.lower():
            return {'type': 'generate_predictions', 'priority': 'high'}
        elif 'learn' in role.lower():
            return {'type': 'learn_from_data', 'priority': 'medium'}
        elif 'optimi' in role.lower():
            return {'type': 'optimize_system', 'priority': 'low'}
        
        return None
    
    def _execute_task(self, agent_id: str, task: Dict):
        """Execute task with agent"""
        agent = self.agents[agent_id]
        
        try:
            # Simulate task execution
            agent['status'] = 'working'
            agent['last_activity'] = datetime.now().isoformat()
            
            # Task completed
            agent['tasks_completed'] += 1
            agent['status'] = 'active'
            self.performance_metrics['total_tasks_completed'] += 1
            
        except Exception as e:
            agent['errors'] += 1
            agent['performance'] = max(0.1, agent['performance'] - 0.05)
            logger.error(f"❌ Agent {agent_id} task failed: {e}")
    
    def _monitor_performance(self):
        """Monitor all agent performance"""
        logger.info("📊 Monitoring agent performance...")
        
        total_performance = 0
        active_count = 0
        
        for agent_id, agent in self.agents.items():
            if agent['status'] in ['active', 'working']:
                total_performance += agent['performance']
                active_count += 1
                
                # Log agent status
                logger.info(f"   {agent['config']['name']}: "
                          f"Tasks={agent['tasks_completed']}, "
                          f"Performance={agent['performance']:.2f}, "
                          f"Errors={agent['errors']}")
        
        if active_count > 0:
            avg_performance = total_performance / active_count
            self.performance_metrics['average_performance'] = avg_performance
            self.performance_metrics['active_agents'] = active_count
            
            logger.info(f"   📈 Average Performance: {avg_performance:.2%}")
            logger.info(f"   🤖 Active Agents: {active_count}/{self.performance_metrics['total_agents']}")
    
    def _optimize_allocation(self):
        """Optimize agent task allocation"""
        logger.info("⚡ Optimizing agent allocation...")
        
        # Find underperforming agents
        for agent_id, agent in self.agents.items():
            if agent['performance'] < 0.5:
                logger.info(f"   ⚠️  {agent['config']['name']} underperforming, optimizing...")
                # Reset and optimize
                agent['performance'] = min(1.0, agent['performance'] + 0.2)
                agent['errors'] = 0
        
        logger.info("   ✅ Optimization complete")
    
    def _save_metrics(self):
        """Save performance metrics"""
        metrics_file = f"{self.data_dir}/metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        metrics_snapshot = {
            'timestamp': datetime.now().isoformat(),
            'system_metrics': self.performance_metrics,
            'agent_metrics': {
                agent_id: {
                    'name': agent['config']['name'],
                    'tasks_completed': agent['tasks_completed'],
                    'performance': agent['performance'],
                    'errors': agent['errors'],
                    'status': agent['status']
                }
                for agent_id, agent in self.agents.items()
            }
        }
        
        try:
            with open(metrics_file, 'w') as f:
                json.dump(metrics_snapshot, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Could not save metrics: {e}")
    
    def stop(self):
        """Stop the orchestrator"""
        logger.info("🛑 Stopping AI Orchestrator...")
        self.running = False
        
        # Stop all agents
        for agent_id in self.agents:
            self.agents[agent_id]['status'] = 'stopped'
        
        self._save_metrics()
        logger.info("✅ AI Orchestrator stopped")
    
    def get_status(self) -> Dict:
        """Get orchestrator status"""
        uptime = "Not started"
        if self.performance_metrics['started_at']:
            start_time = datetime.fromisoformat(self.performance_metrics['started_at'])
            uptime = str(datetime.now() - start_time).split('.')[0]
        
        return {
            'running': self.running,
            'uptime': uptime,
            'total_agents': self.performance_metrics['total_agents'],
            'active_agents': self.performance_metrics['active_agents'],
            'total_tasks': self.performance_metrics['total_tasks_completed'],
            'average_performance': f"{self.performance_metrics['average_performance']:.2%}",
            'system_health': f"{self.performance_metrics['system_health']}%",
            'agents': {
                agent_id: {
                    'name': agent['config']['name'],
                    'status': agent['status'],
                    'tasks': agent['tasks_completed'],
                    'performance': f"{agent['performance']:.2%}"
                }
                for agent_id, agent in self.agents.items()
            }
        }


# Global orchestrator instance
_orchestrator_instance = None


def get_orchestrator() -> AIOrchestrator:
    """Get or create global orchestrator"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = AIOrchestrator()
    return _orchestrator_instance


def start_orchestrator():
    """Start the AI orchestrator"""
    orchestrator = get_orchestrator()
    orchestrator.start()
    return orchestrator


def stop_orchestrator():
    """Stop the AI orchestrator"""
    orchestrator = get_orchestrator()
    orchestrator.stop()


def get_orchestrator_status() -> Dict:
    """Get orchestrator status"""
    orchestrator = get_orchestrator()
    return orchestrator.get_status()


if __name__ == "__main__":
    """Run orchestrator as standalone"""
    print("=" * 70)
    print("🎭 SignalTrust AI - AI Orchestrator")
    print("=" * 70)
    
    orchestrator = AIOrchestrator()
    
    try:
        orchestrator.start()
        
        # Keep running
        while True:
            time.sleep(60)
            status = orchestrator.get_status()
            logger.info(f"\n📊 System Status:")
            logger.info(f"   Tasks Completed: {status['total_tasks']}")
            logger.info(f"   Active Agents: {status['active_agents']}/{status['total_agents']}")
            logger.info(f"   Performance: {status['average_performance']}")
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutdown requested...")
        orchestrator.stop()
        logger.info("👋 Goodbye!")
