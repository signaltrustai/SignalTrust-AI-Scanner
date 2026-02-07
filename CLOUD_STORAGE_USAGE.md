# Cloud Storage Manager - Quick Reference Guide

## Overview
The `cloud_storage_manager.py` provides an AWS S3 backup manager for SignalTrust AI. It creates compressed tar.gz backups of data files and syncs them to cloud storage.

## Global Instance
```python
from cloud_storage_manager import cloud_storage
```

## Core Methods

### 1. backup_all_data()
Creates a unified backup of all data sources in tar.gz format.

```python
backup = cloud_storage.backup_all_data()
# Returns: Dict with backup metadata
# {
#   'backup_id': 'unified_backup_20260207_174929',
#   'local_path': 'backups/unified_backup_20260207_174929.tar.gz',
#   'size_bytes': 840204,
#   'checksum': '2e56b92e5c331a7d...',
#   'metadata_path': 'backups/unified_backup_20260207_174929_metadata.json'
# }
```

**Backed up files:**
- `data/ai_hub.json`
- `data/total_market_intelligence.json`
- `data/discovered_gems.json`
- `data/scanner_history.json`
- `data/user_preferences.json`
- All directories under `data/ai_hub/`, `data/total_market_intelligence/`, `data/notification_ai/`

### 2. sync_to_cloud()
Uploads local backups to AWS S3.

```python
result = cloud_storage.sync_to_cloud()
# Returns: Dict with sync results
# {
#   'synced': ['unified_backup_20260207_174929'],
#   'failed': [],
#   'skipped': []
# }
```

### 3. list_backups(limit)
Lists recent backups.

```python
backups = cloud_storage.list_backups(limit=10)
# Returns: List of backup metadata dicts
for backup in backups:
    print(f"{backup['backup_id']}: {backup['size_bytes']} bytes")
```

### 4. get_statistics()
Returns backup statistics.

```python
stats = cloud_storage.get_statistics()
# Returns: Dict with statistics
# {
#   'total_backups': 2,
#   'total_size_mb': 1.60,
#   'cloud_synced': 0,
#   'provider': 'local',
#   'compression_enabled': True
# }
```

## Configuration (.env file)

### AWS S3 Configuration
```bash
# Required for AWS S3
CLOUD_PROVIDER=aws
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA3XBYYCER25NRMPXG
AWS_SECRET_ACCESS_KEY=3/4rlC8Q6fggtsm3aKjwN43l/dtcvvU9mZFyeAIH
# Optional settings
CLOUD_COMPRESS=true
CLOUD_AUTO_SYNC=true
CLOUD_SYNC_INTERVAL=3600
```

### Environment Setup
1. Copy `.env.example` to `.env`
2. Configure your cloud provider settings
3. Install dependencies: `pip install -r requirements.txt`

## Backup Format

### Filename Format
- Backup: `unified_backup_YYYYMMDD_HHMMSS.tar.gz`
- Metadata: `unified_backup_YYYYMMDD_HHMMSS_metadata.json`

### Directory Structure
```
backups/
├── unified_backup_20260207_174929.tar.gz
├── unified_backup_20260207_174929_metadata.json
└── backup_index.json
```

### Metadata File Content
```json
{
  "backup_id": "unified_backup_20260207_174929",
  "timestamp": "2026-02-07T17:49:29.614861",
  "filename": "unified_backup_20260207_174929.tar.gz",
  "size_bytes": 840204,
  "checksum": "2e56b92e5c331a7d7a72334309140e9a2",
  "format": "tar.gz",
  "files_backed_up": [
    "data/discovered_gems.json",
    "data/ai_hub",
    "data/total_market_intelligence",
    "data/notification_ai"
  ],
  "cloud_sync_status": "pending",
  "cloud_path": "s3://bucket-name/backups/unified_backup_20260207_174929/..."
}
```

## Usage Examples

### Example 1: Create and sync backup
```python
from cloud_storage_manager import cloud_storage

# Create backup
backup = cloud_storage.backup_all_data()
print(f"Backup created: {backup['backup_id']}")

# Sync to S3 (if AWS configured)
if cloud_storage.provider == 'aws':
    result = cloud_storage.sync_to_cloud()
    print(f"Synced {len(result['synced'])} backups")
```

### Example 2: List and retrieve backups
```python
from cloud_storage_manager import cloud_storage

# List recent backups
backups = cloud_storage.list_backups(5)
for b in backups:
    status = "☁️" if b['cloud_synced'] else "💾"
    print(f"{status} {b['backup_id']}")

# Get backup metadata
backup_data = cloud_storage.get_backup('unified_backup_20260207_174929')
print(backup_data)
```

### Example 3: Monitor statistics
```python
from cloud_storage_manager import cloud_storage

stats = cloud_storage.get_statistics()
print(f"Total backups: {stats['total_backups']}")
print(f"Total size: {stats['total_size_mb']:.2f} MB")
print(f"Cloud synced: {stats['cloud_synced']}")
```

## Monitoring Scripts

### monitor_backups.py
Dashboard to view backup status:
```bash
python3 monitor_backups.py
```

### auto_backup.py
Automated backup scheduler:
```bash
python3 auto_backup.py
# Runs backup every 24 hours
# Syncs to cloud every 1 hour (if configured)
```

## Security Notes

⚠️ **IMPORTANT**: Never commit `.env` file with real credentials to version control!

- AWS credentials are read from `.env` file only
- No credentials are hardcoded in the source code
- Use IAM roles when possible (on AWS EC2/Lambda)
- Rotate access keys regularly
- Enable encryption at rest on S3

## Dependencies

Required packages (in requirements.txt):
- `python-dotenv>=0.19.0` - Load .env configuration
- `boto3` (optional) - AWS S3 client
- `schedule>=1.1.0` - For auto_backup.py

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Supported Cloud Providers

1. **AWS S3** (Primary)
   - Set `CLOUD_PROVIDER=aws`
   - Configure AWS credentials in `.env`

2. **Google Cloud Storage** (Optional)
   - Set `CLOUD_PROVIDER=gcp`
   - Configure GCP credentials

3. **Azure Blob Storage** (Optional)
   - Set `CLOUD_PROVIDER=azure`
   - Configure Azure credentials

4. **Local** (Default)
   - Set `CLOUD_PROVIDER=local`
   - No cloud sync, local backups only

## Testing

Run the comprehensive test:
```bash
python3 test_cloud_storage_features.py
```

Run the original test suite:
```bash
python3 test_cloud_storage.py
```

## Troubleshooting

### "boto3 not installed"
```bash
pip install boto3
```

### "AWS credentials not found"
1. Check `.env` file exists
2. Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set
3. Try: `python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.environ.get('AWS_ACCESS_KEY_ID'))"`

### "Backup directory not found"
The `backups/` directory is created automatically on first run.

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```
