#!/usr/bin/env python3
"""
AI Cloud Backup System - AWS S3 Integration
Automatically backs up all AI data to AWS S3 cloud
Les IA sauvegardent TOUT dans AWS automatiquement
"""

import os
import json
import gzip
import shutil
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger('AICloudBackup')


class AICloudBackup:
    """AWS S3 backup system for AI data"""
    
    def __init__(self, bucket_name: str = None, region: str = 'us-east-1'):
        """Initialize cloud backup system
        
        Args:
            bucket_name: S3 bucket name (from env if not provided)
            region: AWS region
        """
        self.bucket_name = bucket_name or os.environ.get('AWS_S3_BUCKET', 'signaltrust-ai-backups')
        self.region = region or os.environ.get('AWS_REGION', 'us-east-1')
        self.compress = os.environ.get('CLOUD_COMPRESS', 'true').lower() == 'true'
        
        # AWS credentials
        self.aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        
        # Initialize S3 client
        self.s3_client = None
        self._init_s3_client()
        
        # Backup paths
        self.backup_paths = {
            'memory': 'data/ai_memory.db',
            'worker_data': 'data/ai_worker/',
            'orchestrator_data': 'data/ai_orchestrator/',
            'logs': 'data/ai_system.log',
            'worker_logs': 'data/ai_worker.log'
        }
        
        logger.info(f"🔐 AI Cloud Backup initialized")
        logger.info(f"   Bucket: {self.bucket_name}")
        logger.info(f"   Region: {self.region}")
        logger.info(f"   Compression: {'Enabled' if self.compress else 'Disabled'}")
    
    def _init_s3_client(self):
        """Initialize S3 client"""
        try:
            import boto3
            
            if self.aws_access_key and self.aws_secret_key:
                # Use explicit credentials
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key,
                    region_name=self.region
                )
                logger.info("✅ S3 client initialized with provided credentials")
            else:
                # Use IAM role or default credentials
                self.s3_client = boto3.client('s3', region_name=self.region)
                logger.info("✅ S3 client initialized with default credentials")
            
            # Verify bucket access
            self._verify_bucket()
            
        except ImportError:
            logger.warning("⚠️  boto3 not installed. Install with: pip install boto3")
            logger.warning("   Cloud backup will not be available")
        except Exception as e:
            logger.error(f"❌ Failed to initialize S3 client: {e}")
            self.s3_client = None
    
    def _verify_bucket(self):
        """Verify bucket exists and is accessible"""
        if not self.s3_client:
            return False
        
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"✅ Bucket {self.bucket_name} is accessible")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Bucket verification failed: {e}")
            logger.warning(f"   Attempting to create bucket...")
            try:
                if self.region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                logger.info(f"✅ Bucket {self.bucket_name} created successfully")
                return True
            except Exception as e2:
                logger.error(f"❌ Failed to create bucket: {e2}")
                return False
    
    def backup_all(self) -> Dict:
        """Backup all AI data to cloud
        
        Returns:
            Backup results
        """
        if not self.s3_client:
            return {
                'success': False,
                'error': 'S3 client not initialized',
                'message': 'Configure AWS credentials to enable cloud backup'
            }
        
        logger.info("☁️  Starting complete AI data backup to AWS S3...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_results = {
            'timestamp': timestamp,
            'bucket': self.bucket_name,
            'files_backed_up': [],
            'total_size_bytes': 0,
            'compressed': self.compress
        }
        
        # Backup memory database
        memory_result = self._backup_memory_database(timestamp)
        if memory_result['success']:
            backup_results['files_backed_up'].append(memory_result)
            backup_results['total_size_bytes'] += memory_result.get('size', 0)
        
        # Backup worker data
        worker_result = self._backup_directory('worker_data', timestamp)
        if worker_result['success']:
            backup_results['files_backed_up'].append(worker_result)
            backup_results['total_size_bytes'] += worker_result.get('size', 0)
        
        # Backup orchestrator data
        orch_result = self._backup_directory('orchestrator_data', timestamp)
        if orch_result['success']:
            backup_results['files_backed_up'].append(orch_result)
            backup_results['total_size_bytes'] += orch_result.get('size', 0)
        
        # Backup logs
        logs_result = self._backup_logs(timestamp)
        if logs_result['success']:
            backup_results['files_backed_up'].append(logs_result)
            backup_results['total_size_bytes'] += logs_result.get('size', 0)
        
        backup_results['success'] = len(backup_results['files_backed_up']) > 0
        
        # Save backup manifest
        self._save_backup_manifest(backup_results)
        
        if backup_results['success']:
            logger.info(f"✅ Backup completed successfully!")
            logger.info(f"   Files backed up: {len(backup_results['files_backed_up'])}")
            logger.info(f"   Total size: {self._format_size(backup_results['total_size_bytes'])}")
        else:
            logger.error("❌ Backup failed - no files backed up")
        
        return backup_results
    
    def _backup_memory_database(self, timestamp: str) -> Dict:
        """Backup memory database to S3
        
        Args:
            timestamp: Backup timestamp
            
        Returns:
            Backup result
        """
        db_path = self.backup_paths['memory']
        
        if not os.path.exists(db_path):
            return {'success': False, 'error': 'Memory database not found'}
        
        logger.info(f"📦 Backing up memory database...")
        
        try:
            # S3 key for database
            s3_key = f"ai_memory/{timestamp}/ai_memory.db"
            
            # Compress if enabled
            if self.compress:
                compressed_path = f"/tmp/ai_memory_{timestamp}.db.gz"
                with open(db_path, 'rb') as f_in:
                    with gzip.open(compressed_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                upload_path = compressed_path
                s3_key += '.gz'
            else:
                upload_path = db_path
            
            # Upload to S3
            file_size = os.path.getsize(upload_path)
            self.s3_client.upload_file(upload_path, self.bucket_name, s3_key)
            
            # Clean up compressed file
            if self.compress and os.path.exists(compressed_path):
                os.remove(compressed_path)
            
            logger.info(f"   ✅ Memory database backed up: {s3_key}")
            
            return {
                'success': True,
                'type': 'memory_database',
                's3_key': s3_key,
                'size': file_size
            }
            
        except Exception as e:
            logger.error(f"   ❌ Failed to backup memory database: {e}")
            return {'success': False, 'error': str(e)}
    
    def _backup_directory(self, dir_key: str, timestamp: str) -> Dict:
        """Backup directory to S3
        
        Args:
            dir_key: Directory key from backup_paths
            timestamp: Backup timestamp
            
        Returns:
            Backup result
        """
        dir_path = self.backup_paths.get(dir_key)
        
        if not dir_path or not os.path.exists(dir_path):
            return {'success': False, 'error': f'Directory {dir_key} not found'}
        
        logger.info(f"📦 Backing up {dir_key}...")
        
        try:
            total_size = 0
            files_count = 0
            
            # Create tar.gz archive
            archive_name = f"/tmp/{dir_key}_{timestamp}.tar.gz"
            import tarfile
            
            with tarfile.open(archive_name, "w:gz") as tar:
                tar.add(dir_path, arcname=os.path.basename(dir_path))
            
            # Upload to S3
            s3_key = f"{dir_key}/{timestamp}/{os.path.basename(archive_name)}"
            file_size = os.path.getsize(archive_name)
            
            self.s3_client.upload_file(archive_name, self.bucket_name, s3_key)
            
            # Clean up
            os.remove(archive_name)
            
            logger.info(f"   ✅ {dir_key} backed up: {s3_key}")
            
            return {
                'success': True,
                'type': dir_key,
                's3_key': s3_key,
                'size': file_size
            }
            
        except Exception as e:
            logger.error(f"   ❌ Failed to backup {dir_key}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _backup_logs(self, timestamp: str) -> Dict:
        """Backup log files to S3
        
        Args:
            timestamp: Backup timestamp
            
        Returns:
            Backup result
        """
        logger.info(f"📦 Backing up logs...")
        
        try:
            log_files = []
            
            # Collect all log files
            for key in ['logs', 'worker_logs']:
                log_path = self.backup_paths.get(key)
                if log_path and os.path.exists(log_path):
                    log_files.append(log_path)
            
            if not log_files:
                return {'success': False, 'error': 'No log files found'}
            
            # Create archive
            archive_name = f"/tmp/logs_{timestamp}.tar.gz"
            import tarfile
            
            with tarfile.open(archive_name, "w:gz") as tar:
                for log_file in log_files:
                    tar.add(log_file, arcname=os.path.basename(log_file))
            
            # Upload to S3
            s3_key = f"logs/{timestamp}/logs.tar.gz"
            file_size = os.path.getsize(archive_name)
            
            self.s3_client.upload_file(archive_name, self.bucket_name, s3_key)
            
            # Clean up
            os.remove(archive_name)
            
            logger.info(f"   ✅ Logs backed up: {s3_key}")
            
            return {
                'success': True,
                'type': 'logs',
                's3_key': s3_key,
                'size': file_size
            }
            
        except Exception as e:
            logger.error(f"   ❌ Failed to backup logs: {e}")
            return {'success': False, 'error': str(e)}
    
    def _save_backup_manifest(self, backup_results: Dict):
        """Save backup manifest to S3
        
        Args:
            backup_results: Backup results
        """
        try:
            manifest_key = f"manifests/backup_{backup_results['timestamp']}.json"
            manifest_data = json.dumps(backup_results, indent=2)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=manifest_key,
                Body=manifest_data.encode('utf-8'),
                ContentType='application/json'
            )
            
            logger.info(f"   ✅ Backup manifest saved: {manifest_key}")
            
        except Exception as e:
            logger.error(f"   ⚠️  Failed to save manifest: {e}")
    
    def list_backups(self, limit: int = 10) -> List[Dict]:
        """List available backups in S3
        
        Args:
            limit: Maximum backups to list
            
        Returns:
            List of backups
        """
        if not self.s3_client:
            return []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='manifests/',
                MaxKeys=limit
            )
            
            backups = []
            for obj in response.get('Contents', []):
                if obj['Key'].endswith('.json'):
                    # Get manifest
                    manifest_obj = self.s3_client.get_object(
                        Bucket=self.bucket_name,
                        Key=obj['Key']
                    )
                    manifest = json.loads(manifest_obj['Body'].read())
                    backups.append(manifest)
            
            # Sort by timestamp
            backups.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return backups[:limit]
            
        except Exception as e:
            logger.error(f"❌ Failed to list backups: {e}")
            return []
    
    def restore_backup(self, timestamp: str) -> Dict:
        """Restore backup from S3
        
        Args:
            timestamp: Backup timestamp to restore
            
        Returns:
            Restore result
        """
        if not self.s3_client:
            return {'success': False, 'error': 'S3 client not initialized'}
        
        logger.info(f"♻️  Restoring backup from {timestamp}...")
        
        try:
            # Get backup manifest
            manifest_key = f"manifests/backup_{timestamp}.json"
            manifest_obj = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=manifest_key
            )
            manifest = json.loads(manifest_obj['Body'].read())
            
            restored_files = []
            
            # Restore each file
            for file_info in manifest.get('files_backed_up', []):
                s3_key = file_info['s3_key']
                
                # Download from S3
                local_path = f"/tmp/restore_{os.path.basename(s3_key)}"
                self.s3_client.download_file(self.bucket_name, s3_key, local_path)
                
                # Extract if compressed
                if s3_key.endswith('.gz') or s3_key.endswith('.tar.gz'):
                    # Handle extraction based on type
                    if 'memory' in s3_key:
                        # Extract memory database
                        import gzip
                        with gzip.open(local_path, 'rb') as f_in:
                            with open(self.backup_paths['memory'], 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                    else:
                        # Extract tar.gz
                        import tarfile
                        with tarfile.open(local_path, 'r:gz') as tar:
                            tar.extractall(path='data/')
                
                restored_files.append(s3_key)
                
                # Clean up
                if os.path.exists(local_path):
                    os.remove(local_path)
            
            logger.info(f"✅ Backup restored successfully!")
            logger.info(f"   Files restored: {len(restored_files)}")
            
            return {
                'success': True,
                'timestamp': timestamp,
                'files_restored': restored_files
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to restore backup: {e}")
            return {'success': False, 'error': str(e)}
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def get_backup_stats(self) -> Dict:
        """Get backup statistics
        
        Returns:
            Backup statistics
        """
        if not self.s3_client:
            return {'error': 'S3 client not initialized'}
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name
            )
            
            total_size = sum(obj['Size'] for obj in response.get('Contents', []))
            total_files = len(response.get('Contents', []))
            
            return {
                'bucket': self.bucket_name,
                'total_files': total_files,
                'total_size': self._format_size(total_size),
                'total_size_bytes': total_size
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {'error': str(e)}


# Global backup instance
_backup_instance = None


def get_cloud_backup() -> AICloudBackup:
    """Get or create global cloud backup instance"""
    global _backup_instance
    if _backup_instance is None:
        _backup_instance = AICloudBackup()
    return _backup_instance


def backup_to_cloud() -> Dict:
    """Backup all AI data to cloud
    
    Returns:
        Backup result
    """
    backup = get_cloud_backup()
    return backup.backup_all()


def list_cloud_backups(limit: int = 10) -> List[Dict]:
    """List cloud backups
    
    Args:
        limit: Maximum backups to list
        
    Returns:
        List of backups
    """
    backup = get_cloud_backup()
    return backup.list_backups(limit)


def restore_from_cloud(timestamp: str) -> Dict:
    """Restore from cloud backup
    
    Args:
        timestamp: Backup timestamp
        
    Returns:
        Restore result
    """
    backup = get_cloud_backup()
    return backup.restore_backup(timestamp)


if __name__ == "__main__":
    # Test cloud backup
    print("☁️  Testing AI Cloud Backup System...")
    
    backup_system = AICloudBackup()
    
    # Test backup
    print("\n📦 Testing backup...")
    result = backup_system.backup_all()
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # List backups
    print("\n📋 Listing backups...")
    backups = backup_system.list_backups()
    print(f"Found {len(backups)} backups")
    
    # Get stats
    print("\n📊 Backup statistics...")
    stats = backup_system.get_backup_stats()
    print(json.dumps(stats, indent=2))
    
    print("\n✅ Cloud backup test complete!")
