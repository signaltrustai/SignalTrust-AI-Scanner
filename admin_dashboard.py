#!/usr/bin/env python3
"""
Admin Dashboard Module
Special admin-only section to monitor everything
- View all backups
- View all AI conversations
- Monitor system status
- Control AI agents
"""

from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from functools import wraps
from datetime import datetime
import json

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin authentication decorator
def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Check if user is admin
        user_id = session.get('user_id')
        user_email = session.get('email')
        
        # Import admin config
        try:
            from config.admin_config import is_admin_user_id, is_admin_email
            
            if not (is_admin_user_id(user_id) or is_admin_email(user_email)):
                return jsonify({'error': 'Access denied - Admin only'}), 403
        except Exception as e:
            # Fallback check
            print(f"⚠️ admin_required: admin config import failed: {e}")
            if user_id != 'owner_admin_001':
                return jsonify({'error': 'Access denied - Admin only'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def admin_dashboard():
    """Main admin dashboard"""
    return render_template('admin_dashboard.html')


@admin_bp.route('/api/system-status')
@admin_required
def get_system_status():
    """Get complete system status"""
    try:
        from ai_system_manager import get_ai_system_status
        from ai_memory_system import get_memory
        
        # Get system status
        system_status = get_ai_system_status()
        
        # Get memory stats
        memory = get_memory()
        memory_stats = memory.get_memory_stats()
        
        # Combine
        status = {
            'system': system_status,
            'memory': memory_stats,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/backups')
@admin_required
def get_backups():
    """Get list of all backups"""
    try:
        from ai_cloud_backup import list_cloud_backups
        
        limit = int(request.args.get('limit', 50))
        backups = list_cloud_backups(limit=limit)
        
        return jsonify({
            'success': True,
            'backups': backups,
            'count': len(backups)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/conversations')
@admin_required
def get_conversations():
    """Get all AI conversations"""
    try:
        from ai_memory_system import get_memory
        
        memory = get_memory()
        user_id = request.args.get('user_id', 'all')
        limit = int(request.args.get('limit', 100))
        
        if user_id == 'all':
            # Get conversations for all users (requires custom query)
            import sqlite3
            conn = sqlite3.connect(memory.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, role, content, ai_type, timestamp
                FROM conversations
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    'user_id': row[0],
                    'role': row[1],
                    'content': row[2],
                    'ai_type': row[3],
                    'timestamp': row[4]
                })
            
            conn.close()
        else:
            conversations = memory.recall_conversations(user_id, limit=limit)
        
        return jsonify({
            'success': True,
            'conversations': conversations,
            'count': len(conversations)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/commands')
@admin_required
def get_commands():
    """Get all executed commands"""
    try:
        from ai_memory_system import get_memory
        
        memory = get_memory()
        status = request.args.get('status')  # pending, completed, failed
        limit = int(request.args.get('limit', 100))
        
        commands = memory.recall_commands(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'commands': commands,
            'count': len(commands)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/learnings')
@admin_required
def get_learnings():
    """Get all AI learnings"""
    try:
        from ai_memory_system import get_memory
        
        memory = get_memory()
        learning_type = request.args.get('type')
        subject = request.args.get('subject')
        limit = int(request.args.get('limit', 100))
        
        learnings = memory.recall_learnings(
            learning_type=learning_type,
            subject=subject,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'learnings': learnings,
            'count': len(learnings)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/predictions')
@admin_required
def get_predictions():
    """Get all AI predictions"""
    try:
        from ai_memory_system import get_memory
        
        memory = get_memory()
        
        # Custom query for predictions
        import sqlite3
        conn = sqlite3.connect(memory.db_path)
        cursor = conn.cursor()
        
        limit = int(request.args.get('limit', 100))
        
        cursor.execute('''
            SELECT symbol, prediction, confidence, timestamp
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        predictions = []
        for row in cursor.fetchall():
            predictions.append({
                'symbol': row[0],
                'prediction': row[1],
                'confidence': row[2],
                'timestamp': row[3]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'count': len(predictions)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/agents')
@admin_required
def get_agents():
    """Get all AI agents status"""
    try:
        from ai_orchestrator import get_orchestrator_status
        
        status = get_orchestrator_status()
        
        return jsonify({
            'success': True,
            'agents': status.get('agents', {}),
            'total_agents': status.get('total_agents', 0),
            'active_agents': status.get('active_agents', 0)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/execute-command', methods=['POST'])
@admin_required
def execute_command():
    """Execute admin command"""
    try:
        from ai_command_system import execute_command as exec_cmd
        
        data = request.get_json()
        command = data.get('command')
        user_id = session.get('user_id', 'admin')
        
        if not command:
            return jsonify({'error': 'Command required'}), 400
        
        result = exec_cmd(user_id, command)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/backup-now', methods=['POST'])
@admin_required
def backup_now():
    """Trigger immediate backup"""
    try:
        from ai_cloud_backup import backup_to_cloud
        
        result = backup_to_cloud()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/search', methods=['GET'])
@admin_required
def search_memory():
    """Search across all AI memory"""
    try:
        from ai_memory_system import get_memory
        
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 50))
        
        if not query:
            return jsonify({'error': 'Query required'}), 400
        
        memory = get_memory()
        results = memory.search_memory(query, limit=limit)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/stats/overview')
@admin_required
def get_stats_overview():
    """Get overview statistics"""
    try:
        from ai_memory_system import get_memory
        from ai_cloud_backup import get_cloud_backup
        
        memory = get_memory()
        backup = get_cloud_backup()
        
        # Memory stats
        memory_stats = memory.get_memory_stats()
        
        # Backup stats
        backup_stats = backup.get_backup_stats()
        
        # System uptime
        from ai_system_manager import get_ai_system_status
        system_status = get_ai_system_status()
        
        overview = {
            'memory': memory_stats,
            'backups': backup_stats,
            'system': {
                'running': system_status.get('running', False),
                'uptime': system_status.get('components', {}).get('orchestrator', {}).get('uptime', 'N/A')
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(overview)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Export blueprint
def register_admin_routes(app):
    """Register admin routes with Flask app"""
    app.register_blueprint(admin_bp)
    print("✅ Admin dashboard routes registered at /admin")
