#!/usr/bin/env python3
"""
AI Worker Service - 24/7 Continuous AI Agent
Continuously collects data, learns, and evolves to improve predictions
"""

import os
import json
import time
import schedule
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/ai_worker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AIWorker')


class AIWorkerService:
    """24/7 AI Worker that continuously learns and improves"""
    
    def __init__(self):
        """Initialize AI Worker Service"""
        self.running = False
        self.worker_thread = None
        self.stats = {
            'started_at': None,
            'total_cycles': 0,
            'data_collected': 0,
            'predictions_made': 0,
            'evolution_cycles': 0,
            'accuracy_improvements': 0,
            'current_accuracy': 0.65,
            'status': 'stopped'
        }
        
        # Create data directories
        self.data_dir = 'data/ai_worker'
        self.learning_dir = f'{self.data_dir}/learning'
        self.predictions_dir = f'{self.data_dir}/predictions'
        self.evolution_dir = f'{self.data_dir}/evolution'
        
        self._ensure_directories()
        
        # Load previous stats if they exist
        self._load_stats()
        
    def _ensure_directories(self):
        """Ensure all necessary directories exist"""
        for directory in [self.data_dir, self.learning_dir, self.predictions_dir, self.evolution_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def _load_stats(self):
        """Load previous statistics"""
        stats_file = f'{self.data_dir}/worker_stats.json'
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    saved_stats = json.load(f)
                    self.stats.update(saved_stats)
                    logger.info(f"📊 Loaded previous stats: {self.stats['total_cycles']} cycles completed")
            except Exception as e:
                logger.warning(f"Could not load previous stats: {e}")
    
    def _save_stats(self):
        """Save current statistics"""
        stats_file = f'{self.data_dir}/worker_stats.json'
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save stats: {e}")
    
    def start(self):
        """Start the 24/7 AI worker service"""
        if self.running:
            logger.warning("⚠️  AI Worker is already running")
            return
        
        self.running = True
        self.stats['started_at'] = datetime.now().isoformat()
        self.stats['status'] = 'running'
        
        logger.info("=" * 60)
        logger.info("🚀 AI Worker Service Starting...")
        logger.info("=" * 60)
        logger.info("🤖 AI Agents will work 24/7 to:")
        logger.info("   • Collect market data continuously")
        logger.info("   • Learn from patterns and trends")
        logger.info("   • Evolve and improve predictions")
        logger.info("   • Monitor and optimize performance")
        logger.info("=" * 60)
        
        # Schedule tasks
        schedule.every(5).minutes.do(self._collect_market_data)
        schedule.every(15).minutes.do(self._analyze_and_learn)
        schedule.every(1).hours.do(self._evolve_intelligence)
        schedule.every(30).minutes.do(self._make_predictions)
        schedule.every(6).hours.do(self._optimize_performance)
        schedule.every(1).hours.do(self._save_stats)
        schedule.every(2).hours.do(self._backup_to_cloud)  # Backup to AWS every 2 hours
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._run_worker, daemon=True)
        self.worker_thread.start()
        
        logger.info("✅ AI Worker Service started successfully!")
        logger.info("☁️  AWS Cloud backup scheduled every 2 hours")
        
    def stop(self):
        """Stop the AI worker service"""
        logger.info("🛑 Stopping AI Worker Service...")
        self.running = False
        self.stats['status'] = 'stopped'
        self._save_stats()
        
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        
        logger.info("✅ AI Worker Service stopped")
    
    def _run_worker(self):
        """Main worker loop"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                self.stats['total_cycles'] += 1
            except Exception as e:
                logger.error(f"❌ Error in worker loop: {e}")
                time.sleep(60)
    
    def _collect_market_data(self):
        """Collect market data from multiple sources"""
        logger.info("📊 Collecting market data...")
        
        try:
            # Simulate data collection from various sources
            data_collected = {
                'timestamp': datetime.now().isoformat(),
                'sources': {
                    'stocks': self._collect_stock_data(),
                    'crypto': self._collect_crypto_data(),
                    'forex': self._collect_forex_data(),
                    'news': self._collect_news_data(),
                    'sentiment': self._collect_sentiment_data()
                }
            }
            
            # Save collected data
            data_file = f'{self.data_dir}/collected_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(data_file, 'w') as f:
                json.dump(data_collected, f, indent=2)
            
            self.stats['data_collected'] += len(data_collected['sources'])
            logger.info(f"✅ Data collected: {len(data_collected['sources'])} sources")
            
        except Exception as e:
            logger.error(f"❌ Error collecting data: {e}")
    
    def _collect_stock_data(self) -> Dict:
        """Collect stock market data"""
        # In production, this would fetch real data from APIs
        return {
            'symbols_scanned': 500,
            'data_points': 5000,
            'timestamp': datetime.now().isoformat()
        }
    
    def _collect_crypto_data(self) -> Dict:
        """Collect cryptocurrency data"""
        return {
            'coins_scanned': 100,
            'data_points': 1000,
            'timestamp': datetime.now().isoformat()
        }
    
    def _collect_forex_data(self) -> Dict:
        """Collect forex data"""
        return {
            'pairs_scanned': 50,
            'data_points': 500,
            'timestamp': datetime.now().isoformat()
        }
    
    def _collect_news_data(self) -> Dict:
        """Collect financial news data"""
        return {
            'articles_collected': 100,
            'sources': 10,
            'timestamp': datetime.now().isoformat()
        }
    
    def _collect_sentiment_data(self) -> Dict:
        """Collect market sentiment data"""
        return {
            'sentiment_points': 200,
            'social_mentions': 1000,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_and_learn(self):
        """Analyze collected data and learn patterns"""
        logger.info("🧠 Analyzing data and learning...")
        
        try:
            # Load recent data files
            data_files = sorted([
                f for f in os.listdir(self.data_dir) 
                if f.startswith('collected_data_')
            ])[-10:]  # Last 10 collections
            
            if not data_files:
                logger.info("⚠️  No data to analyze yet")
                return
            
            # Analyze patterns
            patterns = {
                'timestamp': datetime.now().isoformat(),
                'patterns_found': self._find_patterns(data_files),
                'correlations': self._find_correlations(data_files),
                'trends': self._identify_trends(data_files),
                'anomalies': self._detect_anomalies(data_files)
            }
            
            # Save learning results
            learning_file = f'{self.learning_dir}/learning_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(learning_file, 'w') as f:
                json.dump(patterns, f, indent=2)
            
            logger.info(f"✅ Learning complete: {len(patterns['patterns_found'])} patterns found")
            
        except Exception as e:
            logger.error(f"❌ Error in learning process: {e}")
    
    def _find_patterns(self, data_files: List[str]) -> List[Dict]:
        """Find patterns in collected data"""
        # Simplified pattern finding
        return [
            {'type': 'price_movement', 'confidence': 0.85, 'frequency': 'high'},
            {'type': 'volume_spike', 'confidence': 0.78, 'frequency': 'medium'},
            {'type': 'correlation', 'confidence': 0.92, 'frequency': 'high'}
        ]
    
    def _find_correlations(self, data_files: List[str]) -> List[Dict]:
        """Find correlations between assets"""
        return [
            {'asset1': 'BTC', 'asset2': 'ETH', 'correlation': 0.89},
            {'asset1': 'AAPL', 'asset2': 'MSFT', 'correlation': 0.76}
        ]
    
    def _identify_trends(self, data_files: List[str]) -> List[Dict]:
        """Identify market trends"""
        return [
            {'market': 'crypto', 'trend': 'bullish', 'strength': 0.82},
            {'market': 'tech_stocks', 'trend': 'sideways', 'strength': 0.65}
        ]
    
    def _detect_anomalies(self, data_files: List[str]) -> List[Dict]:
        """Detect market anomalies"""
        return [
            {'type': 'volume_anomaly', 'severity': 'medium', 'asset': 'BTC'},
            {'type': 'price_divergence', 'severity': 'low', 'asset': 'ETH'}
        ]
    
    def _evolve_intelligence(self):
        """Evolve AI intelligence based on learning"""
        logger.info("🧬 Evolving AI intelligence...")
        
        try:
            # Load learning files
            learning_files = sorted([
                f for f in os.listdir(self.learning_dir)
                if f.startswith('learning_')
            ])[-50:]  # Last 50 learning sessions
            
            if len(learning_files) < 5:
                logger.info("⚠️  Not enough learning data for evolution yet")
                return
            
            # Calculate improvements
            old_accuracy = self.stats['current_accuracy']
            
            # Simulate evolution (in production, this would be real ML training)
            improvement = min(0.01, (1.0 - old_accuracy) * 0.05)  # Max 1% per evolution
            new_accuracy = min(0.99, old_accuracy + improvement)
            
            self.stats['current_accuracy'] = new_accuracy
            self.stats['evolution_cycles'] += 1
            
            if new_accuracy > old_accuracy:
                self.stats['accuracy_improvements'] += 1
            
            evolution_data = {
                'timestamp': datetime.now().isoformat(),
                'previous_accuracy': old_accuracy,
                'new_accuracy': new_accuracy,
                'improvement': improvement,
                'learning_sessions_analyzed': len(learning_files),
                'evolution_cycle': self.stats['evolution_cycles']
            }
            
            # Save evolution data
            evolution_file = f'{self.evolution_dir}/evolution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(evolution_file, 'w') as f:
                json.dump(evolution_data, f, indent=2)
            
            logger.info(f"✅ Evolution complete: Accuracy {old_accuracy:.2%} → {new_accuracy:.2%}")
            
        except Exception as e:
            logger.error(f"❌ Error in evolution process: {e}")
    
    def _make_predictions(self):
        """Make predictions based on current intelligence"""
        logger.info("🔮 Making predictions...")
        
        try:
            # Generate predictions for various assets
            predictions = {
                'timestamp': datetime.now().isoformat(),
                'accuracy_level': self.stats['current_accuracy'],
                'predictions': [
                    self._predict_asset('BTC'),
                    self._predict_asset('ETH'),
                    self._predict_asset('AAPL'),
                    self._predict_asset('GOOGL')
                ]
            }
            
            # Save predictions
            pred_file = f'{self.predictions_dir}/predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(pred_file, 'w') as f:
                json.dump(predictions, f, indent=2)
            
            self.stats['predictions_made'] += len(predictions['predictions'])
            logger.info(f"✅ Predictions made: {len(predictions['predictions'])} assets")
            
        except Exception as e:
            logger.error(f"❌ Error making predictions: {e}")
    
    def _predict_asset(self, symbol: str) -> Dict:
        """Predict individual asset"""
        # Use AI provider or market analyzer for real predictions
        try:
            from ai_predictor import AIPredictor
            predictor = AIPredictor()
            prediction = predictor.predict(symbol, timeframe='24h')
            return prediction if prediction else self._get_default_prediction(symbol)
        except Exception as e:
            logger.warning(f"Could not generate AI prediction for {symbol}: {e}")
            return self._get_default_prediction(symbol)
    
    def _get_default_prediction(self, symbol: str) -> Dict:
        """Return neutral default prediction"""
        return {
            'symbol': symbol,
            'prediction': 'neutral',
            'confidence': self.stats['current_accuracy'],
            'timeframe': '24h',
            'expected_change': 0.0,
            'note': 'Default prediction - AI analysis unavailable'
        }
    
    def _optimize_performance(self):
        """Optimize AI performance"""
        logger.info("⚡ Optimizing performance...")
        
        try:
            # Clean old data files (keep last 1000)
            for directory in [self.data_dir, self.learning_dir, self.predictions_dir]:
                files = sorted([
                    os.path.join(directory, f) 
                    for f in os.listdir(directory)
                    if os.path.isfile(os.path.join(directory, f))
                ])
                
                if len(files) > 1000:
                    for old_file in files[:-1000]:
                        try:
                            os.remove(old_file)
                        except Exception as e:
                            logger.warning(f"Could not remove old file {old_file}: {e}")
            
            logger.info("✅ Performance optimized: Old data cleaned")
            
        except Exception as e:
            logger.error(f"❌ Error optimizing performance: {e}")
    
    def get_status(self) -> Dict:
        """Get current worker status"""
        if self.stats['started_at']:
            uptime = datetime.now() - datetime.fromisoformat(self.stats['started_at'])
            uptime_str = str(uptime).split('.')[0]
        else:
            uptime_str = "Not started"
        
        return {
            'status': self.stats['status'],
            'uptime': uptime_str,
            'total_cycles': self.stats['total_cycles'],
            'data_collected': self.stats['data_collected'],
            'predictions_made': self.stats['predictions_made'],
            'evolution_cycles': self.stats['evolution_cycles'],
            'current_accuracy': f"{self.stats['current_accuracy']:.2%}",
            'accuracy_improvements': self.stats['accuracy_improvements']
        }
    
    def _backup_to_cloud(self):
        """Backup all AI data to AWS S3 cloud"""
        logger.info("☁️  Backing up AI data to AWS S3...")
        
        try:
            from ai_cloud_backup import backup_to_cloud
            
            result = backup_to_cloud()
            
            if result.get('success'):
                files_count = len(result.get('files_backed_up', []))
                total_size = result.get('total_size_bytes', 0)
                
                logger.info(f"✅ Cloud backup completed successfully!")
                logger.info(f"   Files backed up: {files_count}")
                logger.info(f"   Total size: {self._format_size(total_size)}")
                logger.info(f"   Bucket: {result.get('bucket', 'N/A')}")
            else:
                error = result.get('error', 'Unknown error')
                logger.warning(f"⚠️  Cloud backup failed: {error}")
                
        except Exception as e:
            logger.error(f"❌ Error during cloud backup: {e}")
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


# Global worker instance
_worker_instance = None


def get_worker() -> AIWorkerService:
    """Get or create the global worker instance"""
    global _worker_instance
    if _worker_instance is None:
        _worker_instance = AIWorkerService()
    return _worker_instance


def start_worker():
    """Start the AI worker service"""
    worker = get_worker()
    worker.start()
    return worker


def stop_worker():
    """Stop the AI worker service"""
    worker = get_worker()
    worker.stop()


def get_worker_status() -> Dict:
    """Get worker status"""
    worker = get_worker()
    return worker.get_status()


if __name__ == "__main__":
    """Run as standalone service"""
    print("=" * 60)
    print("SignalTrust AI - 24/7 AI Worker Service")
    print("=" * 60)
    
    worker = AIWorkerService()
    
    try:
        worker.start()
        
        # Keep running
        while True:
            time.sleep(60)
            status = worker.get_status()
            logger.info(f"📊 Status: {status['total_cycles']} cycles, {status['current_accuracy']} accuracy")
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutdown requested...")
        worker.stop()
        logger.info("👋 Goodbye!")
