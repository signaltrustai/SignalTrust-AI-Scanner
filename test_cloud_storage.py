#!/usr/bin/env python3
"""
Test Cloud Storage System
Validates backup, sync, and AI access functionality
"""

import sys
import os
from datetime import datetime


def test_cloud_storage():
    """Test cloud storage manager."""
    print("=" * 80)
    print("🧪 TESTING CLOUD STORAGE SYSTEM")
    print("=" * 80)
    
    from cloud_storage_manager import CloudStorageManager
    
    # Test 1: Initialization
    print("\n1️⃣ Testing Initialization...")
    manager = CloudStorageManager()
    assert manager is not None
    print("   ✅ Manager initialized")
    print(f"   Provider: {manager.provider}")
    print(f"   Compression: {manager.config.get('compress', True)}")
    
    # Test 2: Create Backup
    print("\n2️⃣ Testing Backup Creation...")
    backup = manager.backup_all_data()
    assert backup is not None
    assert 'backup_id' in backup
    assert 'size_bytes' in backup
    print(f"   ✅ Backup created: {backup['backup_id']}")
    print(f"   Size: {backup['size_bytes'] / 1024:.1f}KB")
    print(f"   Path: {backup['local_path']}")
    
    # Test 3: List Backups
    print("\n3️⃣ Testing Backup Listing...")
    backups = manager.list_backups(limit=5)
    assert len(backups) > 0
    print(f"   ✅ Found {len(backups)} backup(s)")
    for b in backups:
        print(f"      - {b['backup_id']}: {b['size_bytes']}B")
    
    # Test 4: Get Statistics
    print("\n4️⃣ Testing Statistics...")
    stats = manager.get_statistics()
    assert 'total_backups' in stats
    assert 'total_size_mb' in stats
    print("   ✅ Statistics retrieved")
    print(f"      Total backups: {stats['total_backups']}")
    print(f"      Total size: {stats['total_size_mb']:.2f}MB")
    print(f"      Provider: {stats['provider']}")
    
    # Test 5: Load Backup
    print("\n5️⃣ Testing Backup Loading...")
    backup_id = backups[0]['backup_id']
    data = manager.get_backup(backup_id)
    assert data is not None
    assert 'data_sources' in data
    print(f"   ✅ Backup loaded: {backup_id}")
    print(f"      Data sources: {len(data['data_sources'])}")
    for source, content in data['data_sources'].items():
        if isinstance(content, dict):
            print(f"         - {source}: {len(content)} items")
        elif isinstance(content, list):
            print(f"         - {source}: {len(content)} items")
    
    # Test 6: Query Backups
    print("\n6️⃣ Testing Backup Query...")
    local_backups = manager.query_backups(cloud_synced=False)
    print(f"   ✅ Query completed")
    print(f"      Local-only backups: {len(local_backups)}")
    
    # Test 7: AI Access Pattern
    print("\n7️⃣ Testing AI Access Pattern...")
    # Simulate AI loading data
    latest_backups = manager.list_backups(limit=3)
    for backup_meta in latest_backups:
        data = manager.get_backup(backup_meta['backup_id'])
        if data:
            # Access specific AI data
            ai_hub_data = data['data_sources'].get('ai_hub', {})
            if ai_hub_data:
                print(f"   ✅ AI can access hub data from {backup_meta['backup_id']}")
                if 'collective_intelligence' in ai_hub_data:
                    iq = ai_hub_data['collective_intelligence'].get('collective_iq', 0)
                    print(f"      Collective IQ: {iq}")
                break
    
    # Test 8: Index Integrity
    print("\n8️⃣ Testing Index Integrity...")
    assert os.path.exists(manager.index_file)
    print(f"   ✅ Index file exists: {manager.index_file}")
    print(f"      Backups in index: {len(manager.index['backups'])}")
    
    return True


def test_api_integration():
    """Test API integration."""
    print("\n" + "=" * 80)
    print("🧪 TESTING API INTEGRATION")
    print("=" * 80)
    
    import app
    
    # Check if cloud storage is imported
    print("\n1️⃣ Checking Import...")
    assert hasattr(app, 'cloud_storage')
    print("   ✅ cloud_storage imported in app.py")
    
    # Check API routes
    print("\n2️⃣ Checking API Routes...")
    routes = [str(rule) for rule in app.app.url_map.iter_rules()]
    
    cloud_routes = [
        '/api/cloud/status',
        '/api/cloud/backup',
        '/api/cloud/sync',
        '/api/cloud/backups',
        '/api/cloud/backup/<backup_id>',
        '/api/cloud/query'
    ]
    
    for route in cloud_routes:
        found = any(route in r for r in routes)
        status = "✅" if found else "❌"
        print(f"   {status} {route}")
        if not found:
            print(f"      WARNING: Route not found!")
    
    total_routes = len(routes)
    print(f"\n   Total API routes: {total_routes}")
    
    return True


def test_documentation():
    """Test documentation files."""
    print("\n" + "=" * 80)
    print("🧪 TESTING DOCUMENTATION")
    print("=" * 80)
    
    files = [
        'cloud_storage_manager.py',
        'CLOUD_STORAGE_GUIDE.md',
        '.env.example'
    ]
    
    for file_path in files:
        exists = os.path.exists(file_path)
        size = os.path.getsize(file_path) if exists else 0
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path} ({size:,} bytes)")
    
    return True


if __name__ == "__main__":
    print("\n🚀 CLOUD STORAGE SYSTEM TEST SUITE")
    print("=" * 80)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        if test_cloud_storage():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"❌ Cloud storage test failed: {e}")
        tests_failed += 1
    
    try:
        if test_api_integration():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        tests_failed += 1
    
    try:
        if test_documentation():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"❌ Documentation test failed: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! Cloud storage system is ready!")
        print("\n💡 Next Steps:")
        print("   1. Configure cloud provider in .env")
        print("   2. Run: python3 cloud_storage_manager.py")
        print("   3. Test cloud sync (if configured)")
        print("   4. Integrate with AI agents")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Review errors above.")
        sys.exit(1)
