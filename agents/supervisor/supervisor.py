"""
SignalTrust Supervisor Agent EU
Based on Auto-GPT architecture for orchestrating sub-agents
"""
import os
import json
import time
from typing import Dict, Any, List
from datetime import datetime


class SignalTrustSupervisor:
    """
    Supervisor agent that orchestrates sub-agents, 
    controls quotas and restarts failed tasks
    """
    
    def __init__(self):
        self.name = "SignalTrustSuper"
        self.role = "Superviseur qui orchestre les sous-agents, contrôle les quotas et relance les tâches échouées."
        self.api_budget = int(os.getenv("API_BUDGET", "200"))
        self.api_usage = 0
        self.task_history = []
        
    def log(self, message: str):
        """Log a message with timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.task_history.append({
            "timestamp": timestamp,
            "message": message
        })
        
    def check_budget(self) -> bool:
        """Check if we have remaining API budget"""
        if self.api_usage >= self.api_budget:
            self.log(f"⚠️ API budget exhausted: {self.api_usage}/{self.api_budget}")
            return False
        return True
    
    def increment_usage(self, cost: int = 1):
        """Increment API usage"""
        self.api_usage += cost
        self.log(f"📊 API usage: {self.api_usage}/{self.api_budget}")
    
    def monitor_task(self, task_name: str, agent: str) -> Dict[str, Any]:
        """Monitor a task execution"""
        self.log(f"🔍 Monitoring task '{task_name}' on agent '{agent}'")
        
        if not self.check_budget():
            return {
                "status": "failed",
                "reason": "budget_exhausted",
                "task": task_name,
                "agent": agent
            }
        
        # Simulate task execution
        self.increment_usage()
        
        return {
            "status": "success",
            "task": task_name,
            "agent": agent,
            "timestamp": datetime.now().isoformat()
        }
    
    def retry_failed_task(self, task: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """Retry a failed task"""
        task_name = task.get("task", "unknown")
        agent = task.get("agent", "unknown")
        
        for attempt in range(1, max_retries + 1):
            self.log(f"🔄 Retry {attempt}/{max_retries} for task '{task_name}'")
            
            if not self.check_budget():
                return {
                    "status": "failed",
                    "reason": "budget_exhausted",
                    "attempts": attempt
                }
            
            result = self.monitor_task(task_name, agent)
            
            if result["status"] == "success":
                self.log(f"✅ Task '{task_name}' succeeded on attempt {attempt}")
                return result
            
            time.sleep(1)  # Wait before retry
        
        self.log(f"❌ Task '{task_name}' failed after {max_retries} attempts")
        return {
            "status": "failed",
            "reason": "max_retries_exceeded",
            "attempts": max_retries
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get supervisor status"""
        return {
            "name": self.name,
            "role": self.role,
            "api_budget": self.api_budget,
            "api_usage": self.api_usage,
            "budget_remaining": self.api_budget - self.api_usage,
            "tasks_executed": len(self.task_history),
            "timestamp": datetime.now().isoformat()
        }
    
    def run_workflow(self, tasks: List[Dict[str, str]]) -> Dict[str, Any]:
        """Run a workflow of tasks"""
        self.log(f"🚀 Starting workflow with {len(tasks)} tasks")
        
        results = []
        failed_tasks = []
        
        for task in tasks:
            task_name = task.get("name", "unknown")
            agent = task.get("agent", "unknown")
            
            result = self.monitor_task(task_name, agent)
            results.append(result)
            
            if result["status"] == "failed":
                failed_tasks.append(task)
        
        # Retry failed tasks
        if failed_tasks:
            self.log(f"⚠️ {len(failed_tasks)} tasks failed, retrying...")
            for task in failed_tasks:
                retry_result = self.retry_failed_task(task)
                results.append(retry_result)
        
        success_count = sum(1 for r in results if r["status"] == "success")
        
        self.log(f"✅ Workflow completed: {success_count}/{len(results)} tasks successful")
        
        return {
            "status": "completed",
            "total_tasks": len(tasks),
            "successful": success_count,
            "failed": len(results) - success_count,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main supervisor loop"""
    supervisor = SignalTrustSupervisor()
    
    print("=" * 60)
    print(f"SignalTrust Supervisor EU - {supervisor.name}")
    print(f"Role: {supervisor.role}")
    print(f"API Budget: {supervisor.api_budget}")
    print("=" * 60)
    
    # Example workflow
    example_tasks = [
        {"name": "crypto_analysis", "agent": "crypto_agent"},
        {"name": "stock_analysis", "agent": "stock_agent"},
        {"name": "whale_monitoring", "agent": "whale_agent"},
        {"name": "news_aggregation", "agent": "news_agent"}
    ]
    
    result = supervisor.run_workflow(example_tasks)
    
    print("\n" + "=" * 60)
    print("Workflow Result:")
    print(json.dumps(result, indent=2))
    print("=" * 60)
    
    status = supervisor.get_status()
    print("\nSupervisor Status:")
    print(json.dumps(status, indent=2))
    print("=" * 60)


if __name__ == "__main__":
    main()
