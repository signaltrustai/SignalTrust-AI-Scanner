#!/usr/bin/env python3
"""
Cloud Storage Manager - Unified backup system for AI data accessibility
Supports AWS S3, Google Cloud Storage, Azure Blob, and local consolidated storage
"""

import json
import os
import gzip
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib
from pathlib import Path


class CloudStorageManager:
    """Centralized cloud storage manager for all AI backups."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize cloud storage manager.
        
        Args:
            config: Configuration dictionary with cloud provider settings
        """
        self.config = config or self._load_config()
        self.provider = self.config.get('provider', 'local')
        self.local_backup_dir = "data/unified_backups/"
        self.index_file = f"{self.local_backup_dir}backup_index.json"
        
        self._ensure_directories()
        self.index = self._load_index()
        
        # Initialize cloud client if configured
        self.cloud_client = self._init_cloud_client()
    
    def _load_config(self) -> Dict:
        """Load configuration from environment or config file."""
        config = {
            'provider': os.getenv('CLOUD_PROVIDER', 'local'),  # local, aws, gcp, azure
            'compress': os.getenv('CLOUD_COMPRESS', 'true').lower() == 'true',
            'auto_sync': os.getenv('CLOUD_AUTO_SYNC', 'true').lower() == 'true',
            'sync_interval': int(os.getenv('CLOUD_SYNC_INTERVAL', '3600')),  # seconds
        }
        
        # AWS S3 config
        if config['provider'] == 'aws':
            config['aws'] = {
                'bucket': os.getenv('AWS_S3_BUCKET', 'signaltrust-ai-backups'),
                'region': os.getenv('AWS_REGION', 'us-east-1'),
                'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
                'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            }
        
        # Google Cloud Storage config
        elif config['provider'] == 'gcp':
            config['gcp'] = {
                'bucket': os.getenv('GCP_BUCKET', 'signaltrust-ai-backups'),
                'project_id': os.getenv('GCP_PROJECT_ID'),
                'credentials_file': os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
            }
        
        # Azure Blob Storage config
        elif config['provider'] == 'azure':
            config['azure'] = {
                'container': os.getenv('AZURE_CONTAINER', 'signaltrust-ai-backups'),
                'connection_string': os.getenv('AZURE_STORAGE_CONNECTION_STRING'),
                'account_name': os.getenv('AZURE_STORAGE_ACCOUNT'),
                'account_key': os.getenv('AZURE_STORAGE_KEY'),
            }
        
        return config
    
    def _ensure_directories(self):
        """Ensure backup directories exist."""
        os.makedirs(self.local_backup_dir, exist_ok=True)
    
    def _load_index(self) -> Dict:
        """Load backup index."""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'backups': [],
            'statistics': {
                'total_backups': 0,
                'total_size_bytes': 0,
                'last_sync': None,
                'cloud_synced': 0
            }
        }
    
    def _save_index(self):
        """Save backup index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def _init_cloud_client(self):
        """Initialize cloud storage client based on provider."""
        if self.provider == 'local':
            return None
        
        try:
            if self.provider == 'aws':
                return self._init_aws_client()
            elif self.provider == 'gcp':
                return self._init_gcp_client()
            elif self.provider == 'azure':
                return self._init_azure_client()
        except Exception as e:
            print(f"⚠️ Cloud client initialization failed: {e}")
            print(f"   Falling back to local storage")
            self.provider = 'local'
            return None
    
    def _init_aws_client(self):
        """Initialize AWS S3 client."""
        try:
            import boto3
            
            aws_config = self.config['aws']
            
            if aws_config.get('access_key') and aws_config.get('secret_key'):
                client = boto3.client(
                    's3',
                    region_name=aws_config['region'],
                    aws_access_key_id=aws_config['access_key'],
                    aws_secret_access_key=aws_config['secret_key']
                )
            else:
                # Use IAM role or default credentials
                client = boto3.client('s3', region_name=aws_config['region'])
            
            # Test connection
            client.list_buckets()
            
            print(f"✅ AWS S3 client initialized (bucket: {aws_config['bucket']})")
            return client
            
        except ImportError:
            print("⚠️ boto3 not installed. Run: pip install boto3")
            return None
        except Exception as e:
            print(f"⚠️ AWS S3 initialization error: {e}")
            return None
    
    def _init_gcp_client(self):
        """Initialize Google Cloud Storage client."""
        try:
            from google.cloud import storage
            
            gcp_config = self.config['gcp']
            
            if gcp_config.get('credentials_file'):
                client = storage.Client.from_service_account_json(
                    gcp_config['credentials_file']
                )
            else:
                client = storage.Client(project=gcp_config.get('project_id'))
            
            # Test connection
            list(client.list_buckets(max_results=1))
            
            print(f"✅ Google Cloud Storage client initialized (bucket: {gcp_config['bucket']})")
            return client
            
        except ImportError:
            print("⚠️ google-cloud-storage not installed. Run: pip install google-cloud-storage")
            return None
        except Exception as e:
            print(f"⚠️ GCP Storage initialization error: {e}")
            return None
    
    def _init_azure_client(self):
        """Initialize Azure Blob Storage client."""
        try:
            from azure.storage.blob import BlobServiceClient
            
            azure_config = self.config['azure']
            
            if azure_config.get('connection_string'):
                client = BlobServiceClient.from_connection_string(
                    azure_config['connection_string']
                )
            else:
                account_url = f"https://{azure_config['account_name']}.blob.core.windows.net"
                client = BlobServiceClient(
                    account_url=account_url,
                    credential=azure_config['account_key']
                )
            
            # Test connection
            list(client.list_containers(max_results=1))
            
            print(f"✅ Azure Blob Storage client initialized (container: {azure_config['container']})")
            return client
            
        except ImportError:
            print("⚠️ azure-storage-blob not installed. Run: pip install azure-storage-blob")
            return None
        except Exception as e:
            print(f"⚠️ Azure Storage initialization error: {e}")
            return None
    
    def backup_all_data(self) -> Dict:
        """Create unified backup of all AI data.
        
        Returns:
            Backup metadata
        """
        print("🔄 Creating unified backup...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_id = f"unified_backup_{timestamp}"
        
        # Collect all data sources
        data_sources = {
            'ai_hub': self._collect_ai_hub_data(),
            'total_market_intelligence': self._collect_market_data(),
            'notification_ai': self._collect_notification_data(),
            'ai_learning': self._collect_learning_data(),
            'discovered_gems': self._collect_gems_data(),
            'universal_analysis': self._collect_universal_analysis(),
        }
        
        # Create unified backup
        unified_backup = {
            'backup_id': backup_id,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'data_sources': data_sources,
            'metadata': {
                'total_items': sum(len(v) if isinstance(v, (list, dict)) else 1 for v in data_sources.values()),
                'sources_count': len(data_sources),
                'compressed': self.config.get('compress', True)
            }
        }
        
        # Save locally
        local_path = self._save_local_backup(backup_id, unified_backup)
        
        # Calculate checksum
        checksum = self._calculate_checksum(local_path)
        
        # Create backup entry
        backup_entry = {
            'backup_id': backup_id,
            'timestamp': unified_backup['timestamp'],
            'local_path': local_path,
            'size_bytes': os.path.getsize(local_path),
            'checksum': checksum,
            'compressed': self.config.get('compress', True),
            'cloud_synced': False,
            'cloud_path': None,
            'metadata': unified_backup['metadata']
        }
        
        # Add to index
        self.index['backups'].append(backup_entry)
        self.index['statistics']['total_backups'] += 1
        self.index['statistics']['total_size_bytes'] += backup_entry['size_bytes']
        self._save_index()
        
        print(f"✅ Unified backup created: {backup_id}")
        print(f"   Size: {backup_entry['size_bytes'] / 1024 / 1024:.2f}MB")
        print(f"   Path: {local_path}")
        
        # Sync to cloud if enabled
        if self.config.get('auto_sync') and self.cloud_client:
            self.sync_to_cloud(backup_id)
        
        return backup_entry
    
    def _collect_ai_hub_data(self) -> Dict:
        """Collect AI Hub data."""
        data = {}
        
        files = [
            'data/ai_hub/shared_knowledge.json',
            'data/ai_hub/collective_intelligence.json',
            'data/ai_hub/communication_log.json'
        ]
        
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        key = Path(file_path).stem
                        data[key] = json.load(f)
                except:
                    pass
        
        return data
    
    def _collect_market_data(self) -> Dict:
        """Collect market intelligence data."""
        data = {}
        
        # Learning data
        files = [
            'data/total_market_intelligence/learning/ai_brain.json',
            'data/total_market_intelligence/learning/ai_evolution_data.json',
            'data/total_market_intelligence/learning/learned_patterns.json'
        ]
        
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        key = Path(file_path).stem
                        data[key] = json.load(f)
                except:
                    pass
        
        # Latest complete market data (most recent)
        complete_dir = 'data/total_market_intelligence/'
        if os.path.exists(complete_dir):
            complete_files = [f for f in os.listdir(complete_dir) if f.startswith('complete_market_data_')]
            if complete_files:
                latest = sorted(complete_files)[-1]
                try:
                    with open(os.path.join(complete_dir, latest), 'r') as f:
                        data['latest_complete_data'] = json.load(f)
                except:
                    pass
        
        return data
    
    def _collect_notification_data(self) -> Dict:
        """Collect notification AI data."""
        data = {}
        
        files = [
            'data/notification_ai/notification_history.json',
            'data/notification_ai/ai_learning.json'
        ]
        
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        key = Path(file_path).stem
                        data[key] = json.load(f)
                except:
                    pass
        
        return data
    
    def _collect_learning_data(self) -> Dict:
        """Collect AI learning data."""
        if os.path.exists('data/ai_learning_data.json'):
            try:
                with open('data/ai_learning_data.json', 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _collect_gems_data(self) -> Dict:
        """Collect discovered gems data."""
        if os.path.exists('data/discovered_gems.json'):
            try:
                with open('data/discovered_gems.json', 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _collect_universal_analysis(self) -> Dict:
        """Collect universal market analysis."""
        if os.path.exists('data/universal_market_analysis.json'):
            try:
                with open('data/universal_market_analysis.json', 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_local_backup(self, backup_id: str, data: Dict) -> str:
        """Save backup locally with optional compression.
        
        Args:
            backup_id: Backup identifier
            data: Data to backup
            
        Returns:
            Path to saved file
        """
        if self.config.get('compress', True):
            file_path = f"{self.local_backup_dir}{backup_id}.json.gz"
            with gzip.open(file_path, 'wt', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        else:
            file_path = f"{self.local_backup_dir}{backup_id}.json"
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        
        return file_path
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def sync_to_cloud(self, backup_id: Optional[str] = None) -> Dict:
        """Sync backup(s) to cloud storage.
        
        Args:
            backup_id: Specific backup to sync, or None for all unsynced
            
        Returns:
            Sync results
        """
        if not self.cloud_client:
            return {'success': False, 'error': 'No cloud client configured'}
        
        if backup_id:
            backups_to_sync = [b for b in self.index['backups'] if b['backup_id'] == backup_id]
        else:
            backups_to_sync = [b for b in self.index['backups'] if not b['cloud_synced']]
        
        results = {
            'synced': [],
            'failed': [],
            'skipped': []
        }
        
        for backup in backups_to_sync:
            try:
                if not os.path.exists(backup['local_path']):
                    results['skipped'].append(backup['backup_id'])
                    continue
                
                cloud_path = self._upload_to_cloud(backup['local_path'], backup['backup_id'])
                
                if cloud_path:
                    backup['cloud_synced'] = True
                    backup['cloud_path'] = cloud_path
                    results['synced'].append(backup['backup_id'])
                    
                    self.index['statistics']['cloud_synced'] += 1
                else:
                    results['failed'].append(backup['backup_id'])
                    
            except Exception as e:
                print(f"⚠️ Failed to sync {backup['backup_id']}: {e}")
                results['failed'].append(backup['backup_id'])
        
        self.index['statistics']['last_sync'] = datetime.now().isoformat()
        self._save_index()
        
        print(f"☁️ Cloud sync complete:")
        print(f"   Synced: {len(results['synced'])}")
        print(f"   Failed: {len(results['failed'])}")
        print(f"   Skipped: {len(results['skipped'])}")
        
        return results
    
    def _upload_to_cloud(self, local_path: str, backup_id: str) -> Optional[str]:
        """Upload file to cloud storage.
        
        Args:
            local_path: Local file path
            backup_id: Backup identifier
            
        Returns:
            Cloud path if successful, None otherwise
        """
        try:
            if self.provider == 'aws':
                return self._upload_to_s3(local_path, backup_id)
            elif self.provider == 'gcp':
                return self._upload_to_gcs(local_path, backup_id)
            elif self.provider == 'azure':
                return self._upload_to_azure(local_path, backup_id)
        except Exception as e:
            print(f"⚠️ Upload error: {e}")
            return None
    
    def _upload_to_s3(self, local_path: str, backup_id: str) -> Optional[str]:
        """Upload to AWS S3."""
        bucket = self.config['aws']['bucket']
        key = f"backups/{backup_id}/{Path(local_path).name}"
        
        self.cloud_client.upload_file(local_path, bucket, key)
        
        cloud_path = f"s3://{bucket}/{key}"
        print(f"   ✅ Uploaded to S3: {cloud_path}")
        return cloud_path
    
    def _upload_to_gcs(self, local_path: str, backup_id: str) -> Optional[str]:
        """Upload to Google Cloud Storage."""
        bucket_name = self.config['gcp']['bucket']
        bucket = self.cloud_client.bucket(bucket_name)
        blob_name = f"backups/{backup_id}/{Path(local_path).name}"
        blob = bucket.blob(blob_name)
        
        blob.upload_from_filename(local_path)
        
        cloud_path = f"gs://{bucket_name}/{blob_name}"
        print(f"   ✅ Uploaded to GCS: {cloud_path}")
        return cloud_path
    
    def _upload_to_azure(self, local_path: str, backup_id: str) -> Optional[str]:
        """Upload to Azure Blob Storage."""
        container_name = self.config['azure']['container']
        blob_name = f"backups/{backup_id}/{Path(local_path).name}"
        
        blob_client = self.cloud_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )
        
        with open(local_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        cloud_path = f"azure://{container_name}/{blob_name}"
        print(f"   ✅ Uploaded to Azure: {cloud_path}")
        return cloud_path
    
    def get_backup(self, backup_id: str, from_cloud: bool = False) -> Optional[Dict]:
        """Retrieve backup by ID.
        
        Args:
            backup_id: Backup identifier
            from_cloud: Load from cloud if True, local if False
            
        Returns:
            Backup data or None
        """
        backup_entry = next((b for b in self.index['backups'] if b['backup_id'] == backup_id), None)
        
        if not backup_entry:
            print(f"⚠️ Backup not found: {backup_id}")
            return None
        
        if from_cloud and backup_entry['cloud_synced']:
            return self._download_from_cloud(backup_entry)
        else:
            return self._load_local_backup(backup_entry)
    
    def _load_local_backup(self, backup_entry: Dict) -> Optional[Dict]:
        """Load backup from local storage."""
        local_path = backup_entry['local_path']
        
        if not os.path.exists(local_path):
            print(f"⚠️ Local backup file not found: {local_path}")
            return None
        
        try:
            if backup_entry.get('compressed', True):
                with gzip.open(local_path, 'rt', encoding='utf-8') as f:
                    return json.load(f)
            else:
                with open(local_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading backup: {e}")
            return None
    
    def _download_from_cloud(self, backup_entry: Dict) -> Optional[Dict]:
        """Download and load backup from cloud."""
        # For now, just load from local if available
        # In production, would download from cloud if local not available
        return self._load_local_backup(backup_entry)
    
    def list_backups(self, limit: int = 10) -> List[Dict]:
        """List available backups.
        
        Args:
            limit: Maximum number of backups to return
            
        Returns:
            List of backup metadata
        """
        backups = sorted(
            self.index['backups'],
            key=lambda x: x['timestamp'],
            reverse=True
        )
        
        return backups[:limit]
    
    def get_statistics(self) -> Dict:
        """Get backup statistics."""
        return {
            'total_backups': self.index['statistics']['total_backups'],
            'total_size_mb': self.index['statistics']['total_size_bytes'] / 1024 / 1024,
            'cloud_synced': self.index['statistics']['cloud_synced'],
            'last_sync': self.index['statistics']['last_sync'],
            'provider': self.provider,
            'compression_enabled': self.config.get('compress', True)
        }
    
    def query_backups(self, **filters) -> List[Dict]:
        """Query backups with filters.
        
        Args:
            **filters: Filter criteria (timestamp, cloud_synced, etc.)
            
        Returns:
            Filtered backups
        """
        backups = self.index['backups']
        
        for key, value in filters.items():
            backups = [b for b in backups if b.get(key) == value]
        
        return backups


# Global instance
cloud_storage = CloudStorageManager()


if __name__ == "__main__":
    manager = CloudStorageManager()
    
    print("=" * 80)
    print("☁️ CLOUD STORAGE MANAGER")
    print("=" * 80)
    
    # Show configuration
    print(f"\n📋 Configuration:")
    print(f"   Provider: {manager.provider}")
    print(f"   Compression: {manager.config.get('compress', True)}")
    print(f"   Auto-sync: {manager.config.get('auto_sync', True)}")
    
    # Create backup
    print("\n🔄 Creating unified backup...")
    backup = manager.backup_all_data()
    
    # Show statistics
    print("\n📊 Statistics:")
    stats = manager.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # List backups
    print("\n📁 Recent Backups:")
    for backup in manager.list_backups(5):
        print(f"   • {backup['backup_id']}")
        print(f"     Size: {backup['size_bytes'] / 1024:.1f}KB")
        print(f"     Cloud: {'✅' if backup['cloud_synced'] else '❌'}")
