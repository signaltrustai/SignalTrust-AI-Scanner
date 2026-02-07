#!/usr/bin/env python3
"""
Test Backup Script
Tests cloud storage initialization, creates a backup, and syncs to AWS S3
"""

import os
import sys
from datetime import datetime
from cloud_storage_manager import CloudStorageManager


def print_separator():
    """Print visual separator."""
    print("=" * 70)


def print_section(title):
    """Print section header."""
    print(f"\n{title}")
    print("-" * 70)


def main():
    """Main test function."""
    print_separator()
    print("🧪 SIGNALTRUST AI - BACKUP TEST SUITE")
    print_separator()
    
    # Initialize cloud storage manager
    print_section("📦 1. Initializing Cloud Storage")
    try:
        manager = CloudStorageManager()
        print(f"✅ Cloud Storage Manager initialized")
        print(f"   Provider: {manager.provider}")
        print(f"   Compression: {manager.config.get('compress', True)}")
        print(f"   Auto-sync: {manager.config.get('auto_sync', True)}")
        
        # Show AWS configuration if available
        if manager.provider == 'aws' and 'aws' in manager.config:
            aws_config = manager.config['aws']
            print(f"   AWS Bucket: {aws_config.get('bucket', 'N/A')}")
            print(f"   AWS Region: {aws_config.get('region', 'N/A')}")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Show current statistics
    print_section("📊 2. Current Statistics")
    try:
        stats = manager.get_statistics()
        print(f"✅ Statistics retrieved:")
        print(f"   Total backups: {stats['total_backups']}")
        print(f"   Total size: {stats['total_size_mb']:.2f} MB")
        print(f"   Cloud synced: {stats['cloud_synced']}")
        print(f"   Provider: {stats['provider']}")
        if stats.get('last_sync'):
            print(f"   Last sync: {stats['last_sync']}")
        else:
            print(f"   Last sync: Never")
    except Exception as e:
        print(f"❌ Failed to get statistics: {e}")
    
    # Create a backup
    print_section("🔄 3. Creating Backup")
    try:
        backup = manager.backup_all_data()
        print(f"✅ Backup created successfully!")
        print(f"   Backup ID: {backup['backup_id']}")
        print(f"   Size: {backup['size_bytes'] / 1024 / 1024:.2f} MB")
        print(f"   Files: {backup['files_count']}")
        print(f"   Checksum: {backup['checksum']}")
        print(f"   Cloud synced: {'Yes' if backup['cloud_synced'] else 'No'}")
        if backup.get('cloud_path'):
            print(f"   Cloud path: {backup['cloud_path']}")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Sync to cloud if not already synced
    print_section("☁️  4. Cloud Sync Status")
    if manager.provider != 'local' and manager.cloud_client:
        if not backup['cloud_synced']:
            print("🔄 Syncing to cloud...")
            try:
                results = manager.sync_to_cloud(backup['backup_id'])
                if backup['backup_id'] in results['synced']:
                    print(f"✅ Successfully synced to {manager.provider.upper()}")
                    # Get updated backup info
                    for b in manager.index['backups']:
                        if b['backup_id'] == backup['backup_id']:
                            if b.get('cloud_path'):
                                print(f"   Cloud path: {b['cloud_path']}")
                            break
                elif backup['backup_id'] in results['failed']:
                    print(f"❌ Failed to sync to cloud")
                else:
                    print(f"⚠️  Sync status unknown")
            except Exception as e:
                print(f"❌ Cloud sync error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✅ Already synced to {manager.provider.upper()}")
            if backup.get('cloud_path'):
                print(f"   Cloud path: {backup['cloud_path']}")
    else:
        print("⚠️  Cloud sync disabled (provider: local)")
        print("   To enable cloud sync:")
        print("   1. Set CLOUD_PROVIDER=aws in .env")
        print("   2. Configure AWS credentials")
        print("   3. Run this test again")
    
    # Display results summary
    print_section("📋 5. Test Results Summary")
    updated_stats = manager.get_statistics()
    print(f"✅ Test completed successfully!")
    print(f"   Provider: {updated_stats['provider']}")
    print(f"   Total backups: {updated_stats['total_backups']}")
    print(f"   Total size: {updated_stats['total_size_mb']:.2f} MB")
    print(f"   Cloud synced: {updated_stats['cloud_synced']}")
    
    # List recent backups
    print_section("📦 6. Recent Backups")
    backups = manager.list_backups(5)
    if backups:
        for i, b in enumerate(backups, 1):
            status = "☁️" if b.get('cloud_synced') else "💾"
            size_mb = b.get('size_bytes', 0) / 1024 / 1024
            print(f"{status} #{i}. {b['backup_id']}")
            print(f"      Time: {b['timestamp']}")
            print(f"      Size: {size_mb:.2f} MB")
            print(f"      Files: {b.get('files_count', 'N/A')}")
    else:
        print("   No backups found")
    
    print_separator()
    print("✅ All tests completed!")
    print_separator()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
