#!/usr/bin/env python3
"""
Automated Backup System
Schedules regular backups and cloud sync for SignalTrust AI
"""

from cloud_storage_manager import cloud_storage
import schedule
import time
from datetime import datetime

def backup_job():
    """Create a complete backup of all data."""
    print(f"\n⏰ Running scheduled backup... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    try:
        result = cloud_storage.backup_all_data()
        if result:
            print("✅ Backup completed successfully")
        else:
            print("⚠️ Backup completed with warnings")
    except Exception as e:
        print(f"❌ Backup failed: {e}")

def sync_job():
    """Sync backups to cloud storage."""
    print(f"\n☁️  Running cloud sync... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    try:
        result = cloud_storage.sync_to_cloud()
        if result:
            print("✅ Cloud sync completed")
        else:
            print("⚠️ Cloud sync completed with warnings")
    except Exception as e:
        print(f"❌ Cloud sync failed: {e}")

# Schedule jobs
# Backup every 24 hours
schedule.every(24).hours.do(backup_job)

# Sync every hour (if cloud is configured)
if cloud_storage.provider != 'local':
    schedule.every(1).hours.do(sync_job)

print("=" * 70)
print("🤖 SIGNALTRUST AI - AUTO-BACKUP SYSTEM")
print("=" * 70)
print(f"\n📅 Schedule:")
print(f"   • Full backup: Every 24 hours")
if cloud_storage.provider != 'local':
    print(f"   • Cloud sync: Every 1 hour")
    print(f"   • Provider: {cloud_storage.provider.upper()}")
else:
    print(f"   • Cloud sync: Disabled (local mode)")
print(f"\n🚀 System started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Run initial backup
print("\n🔄 Running initial backup...")
backup_job()

if cloud_storage.provider != 'local' and cloud_storage.cloud_client:
    print("\n🔄 Running initial sync...")
    sync_job()

print("\n⏰ Scheduler active. Press Ctrl+C to stop.\n")

# Main loop
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    print("\n\n🛑 Auto-backup system stopped by user")
    print("=" * 70)
