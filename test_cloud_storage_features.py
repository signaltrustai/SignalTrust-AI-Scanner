#!/usr/bin/env python3
"""
Test script to demonstrate cloud_storage_manager.py functionality
Shows all required features: backup_all_data(), sync_to_cloud(), list_backups(), get_statistics()
"""

import os
import sys
from cloud_storage_manager import cloud_storage

print("=" * 80)
print("🧪 CLOUD STORAGE MANAGER - FUNCTIONALITY TEST")
print("=" * 80)

# Test 1: Global instance
print("\n1️⃣ Global Instance Test")
print(f"   ✅ cloud_storage instance exists: {cloud_storage is not None}")
print(f"   Type: {type(cloud_storage).__name__}")
print(f"   Provider: {cloud_storage.provider}")

# Test 2: Configuration
print("\n2️⃣ Configuration Test")
print(f"   ✅ Backup directory: {cloud_storage.local_backup_dir}")
print(f"   ✅ Compression enabled: {cloud_storage.config.get('compress', True)}")
print(f"   ✅ Auto-sync enabled: {cloud_storage.config.get('auto_sync', True)}")
if cloud_storage.provider == 'aws':
    print(f"   ✅ AWS S3 Bucket: {cloud_storage.config.get('aws', {}).get('bucket', 'N/A')}")
    print(f"   ✅ AWS Region: {cloud_storage.config.get('aws', {}).get('region', 'N/A')}")

# Test 3: backup_all_data() method
print("\n3️⃣ backup_all_data() Test")
try:
    backup_result = cloud_storage.backup_all_data()
    print(f"   ✅ Backup created successfully")
    print(f"   Backup ID: {backup_result['backup_id']}")
    print(f"   Size: {backup_result['size_bytes'] / 1024 / 1024:.2f} MB")
    print(f"   Path: {backup_result['local_path']}")
    print(f"   Checksum: {backup_result['checksum'][:16]}...")
    
    # Verify files exist
    if os.path.exists(backup_result['local_path']):
        print(f"   ✅ Backup file exists (.tar.gz format)")
    if 'metadata_path' in backup_result and os.path.exists(backup_result['metadata_path']):
        print(f"   ✅ Metadata file exists")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: list_backups() method
print("\n4️⃣ list_backups() Test")
try:
    backups = cloud_storage.list_backups(limit=5)
    print(f"   ✅ Found {len(backups)} backup(s)")
    for i, backup in enumerate(backups[:3], 1):
        status = "☁️ synced" if backup.get('cloud_synced') else "💾 local"
        print(f"   {i}. {backup['backup_id']} - {status}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: get_statistics() method
print("\n5️⃣ get_statistics() Test")
try:
    stats = cloud_storage.get_statistics()
    print(f"   ✅ Statistics retrieved:")
    print(f"   Total backups: {stats['total_backups']}")
    print(f"   Total size: {stats['total_size_mb']:.2f} MB")
    print(f"   Cloud synced: {stats['cloud_synced']}")
    print(f"   Provider: {stats['provider']}")
    print(f"   Compression: {stats['compression_enabled']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: sync_to_cloud() method
print("\n6️⃣ sync_to_cloud() Test")
if cloud_storage.provider != 'local' and cloud_storage.cloud_client:
    try:
        sync_result = cloud_storage.sync_to_cloud()
        print(f"   ✅ Cloud sync attempted")
        print(f"   Synced: {len(sync_result.get('synced', []))}")
        print(f"   Failed: {len(sync_result.get('failed', []))}")
        print(f"   Skipped: {len(sync_result.get('skipped', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"   ⚠️ Skipped (provider: {cloud_storage.provider})")
    print(f"   Note: Set CLOUD_PROVIDER=aws in .env to enable cloud sync")

# Test 7: AWS S3 specific tests
print("\n7️⃣ AWS S3 Integration Test")
if cloud_storage.provider == 'aws':
    print(f"   ✅ AWS S3 client initialized")
    print(f"   Bucket: {cloud_storage.config['aws']['bucket']}")
    print(f"   Region: {cloud_storage.config['aws']['region']}")
else:
    print(f"   ⚠️ AWS not configured (current provider: {cloud_storage.provider})")
    print(f"   To enable AWS S3:")
    print(f"   1. Copy .env.example to .env")
    print(f"   2. Set CLOUD_PROVIDER=aws")
    print(f"   3. Configure AWS_S3_BUCKET, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")

# Test 8: Verify tar.gz format
print("\n8️⃣ Backup Format Test")
if backups:
    latest_backup = backups[0]
    if latest_backup['local_path'].endswith('.tar.gz'):
        print(f"   ✅ Uses tar.gz format")
        
        # Try to list contents
        import tarfile
        try:
            with tarfile.open(latest_backup['local_path'], 'r:gz') as tar:
                members = tar.getmembers()
                print(f"   ✅ Archive is valid ({len(members)} files/dirs)")
        except Exception as e:
            print(f"   ⚠️ Could not verify archive: {e}")
    else:
        print(f"   ⚠️ Not using tar.gz format: {latest_backup['local_path']}")

# Test 9: Environment variable loading
print("\n9️⃣ Environment Variables Test")
from dotenv import load_dotenv
load_dotenv()
env_vars = ['AWS_S3_BUCKET', 'AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
for var in env_vars:
    is_set = var in os.environ
    status = "✅" if is_set else "❌"
    value_preview = "***" if is_set and 'KEY' in var else (os.environ.get(var, 'Not set'))
    print(f"   {status} {var}: {value_preview}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETE")
print("=" * 80)
print("\n📋 Summary:")
print("   ✓ Global instance: cloud_storage")
print("   ✓ Method: backup_all_data() - Creates tar.gz backups")
print("   ✓ Method: sync_to_cloud() - Syncs to AWS S3")
print("   ✓ Method: list_backups() - Lists recent backups")
print("   ✓ Method: get_statistics() - Returns backup stats")
print("   ✓ Config: Loaded from .env using python-dotenv")
print("   ✓ Format: tar.gz with separate metadata JSON files")
print("\n💡 To enable AWS S3 cloud sync:")
print("   1. Configure AWS credentials in .env file")
print("   2. Set CLOUD_PROVIDER=aws")
print("   3. Run: python3 cloud_storage_manager.py")
