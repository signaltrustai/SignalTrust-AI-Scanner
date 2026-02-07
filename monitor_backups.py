#!/usr/bin/env python3
"""
Backup Monitoring Dashboard
Displays backup statistics and recent backups for SignalTrust AI
"""

from cloud_storage_manager import cloud_storage
import json
from datetime import datetime

print("=" * 70)
print("📊 SIGNALTRUST AI - BACKUP DASHBOARD")
print("=" * 70)

try:
    stats = cloud_storage.get_statistics()
    print(f"\n📈 Provider: {stats['provider'].upper()}")
    print(f"📦 Total backups: {stats['total_backups']}")
    print(f"💾 Total size: {stats['total_size_mb']:.2f} MB")
    print(f"☁️  Cloud synced: {stats['cloud_synced']}/{stats['total_backups']}")
    
    if stats.get('last_sync'):
        print(f"🕒 Last sync: {stats['last_sync']}")
    
    backups = cloud_storage.list_backups(10)
    if backups:
        print(f"\n📦 Recent Backups:")
        for b in backups:
            status = "☁️" if b.get('cloud_synced') else "💾"
            size_mb = b.get('size_bytes', 0) / 1024 / 1024
            print(f"   {status} {b['backup_id']}")
            print(f"      Time: {b['timestamp']}")
            print(f"      Size: {size_mb:.2f} MB")
            if 'files_count' in b:
                print(f"      Files: {b['files_count']}")
    else:
        print("\n⚠️  No backups found")
    
    print("\n" + "=" * 70)
    print("✅ Dashboard ready")
    
except Exception as e:
    print(f"\n❌ Error accessing backup system: {e}")
    import traceback
    traceback.print_exc()
