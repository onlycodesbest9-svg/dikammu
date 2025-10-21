"""
Data Management for Users, Progress, and Lessons
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .config import Config


class DataManager:
    """Manages user data, progress, and lesson content"""
    
    _db_path = None
    _conn = None
    
    @classmethod
    def initialize(cls):
        """Initialize database and create tables"""
        data_dir = Config.get_data_dir()
        cls._db_path = data_dir / "recursivelearn.db"
        cls._create_tables()
    
    @classmethod
    def _get_connection(cls):
        """Get database connection"""
        if cls._conn is None:
            cls._conn = sqlite3.connect(cls._db_path, check_same_thread=False)
            cls._conn.row_factory = sqlite3.Row
        return cls._conn
    
    @classmethod
    def _create_tables(cls):
        """Create database tables"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                is_instructor INTEGER DEFAULT 0
            )
        ''')
        
        # Progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                user_id TEXT,
                lesson_id TEXT,
                completed INTEGER DEFAULT 0,
                score REAL DEFAULT 0,
                last_accessed TEXT,
                PRIMARY KEY (user_id, lesson_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Badges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS badges (
                user_id TEXT,
                badge_name TEXT,
                earned_at TEXT,
                PRIMARY KEY (user_id, badge_name),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Saved problems table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                problem_text TEXT,
                solution TEXT,
                saved_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Quiz results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                lesson_id TEXT,
                score REAL,
                total_questions INTEGER,
                completed_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Room members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_members (
                room_code TEXT,
                user_id TEXT,
                joined_at TEXT,
                PRIMARY KEY (room_code, user_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
    
    @classmethod
    def register_user(cls, user_id: str, username: str) -> bool:
        """Register a new user"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if cursor.fetchone():
                return False
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (id, username, created_at, last_login)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
    
    @classmethod
    def login_user(cls, user_id: str, username: str) -> bool:
        """Login a user (verify credentials)"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row and row['username'] == username:
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = ? WHERE id = ?
                ''', (datetime.now().isoformat(), user_id))
                conn.commit()
                return True
            
            return False
        except Exception as e:
            print(f"Error logging in user: {e}")
            return False
    
    @classmethod
    def get_user(cls, user_id: str) -> Optional[Dict]:
        """Get user information"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @classmethod
    def update_progress(cls, user_id: str, lesson_id: str, completed: bool = False, score: float = 0):
        """Update user progress for a lesson"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO progress 
                (user_id, lesson_id, completed, score, last_accessed)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, lesson_id, 1 if completed else 0, score, datetime.now().isoformat()))
            
            conn.commit()
        except Exception as e:
            print(f"Error updating progress: {e}")
    
    @classmethod
    def get_progress(cls, user_id: str) -> List[Dict]:
        """Get all progress for a user"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM progress WHERE user_id = ?
                ORDER BY last_accessed DESC
            ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting progress: {e}")
            return []
    
    @classmethod
    def award_badge(cls, user_id: str, badge_name: str):
        """Award a badge to a user"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO badges (user_id, badge_name, earned_at)
                VALUES (?, ?, ?)
            ''', (user_id, badge_name, datetime.now().isoformat()))
            
            conn.commit()
        except Exception as e:
            print(f"Error awarding badge: {e}")
    
    @classmethod
    def get_badges(cls, user_id: str) -> List[Dict]:
        """Get all badges for a user"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM badges WHERE user_id = ?
                ORDER BY earned_at DESC
            ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting badges: {e}")
            return []
    
    @classmethod
    def save_problem(cls, user_id: str, problem_text: str, solution: str):
        """Save a problem and its solution"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO saved_problems (user_id, problem_text, solution, saved_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, problem_text, solution, datetime.now().isoformat()))
            
            conn.commit()
        except Exception as e:
            print(f"Error saving problem: {e}")
    
    @classmethod
    def get_saved_problems(cls, user_id: str) -> List[Dict]:
        """Get all saved problems for a user"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM saved_problems WHERE user_id = ?
                ORDER BY saved_at DESC
            ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting saved problems: {e}")
            return []
    
    @classmethod
    def save_quiz_result(cls, user_id: str, lesson_id: str, score: float, total: int):
        """Save a quiz result"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO quiz_results (user_id, lesson_id, score, total_questions, completed_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, lesson_id, score, total, datetime.now().isoformat()))
            
            conn.commit()
        except Exception as e:
            print(f"Error saving quiz result: {e}")
    
    @classmethod
    def get_leaderboard(cls) -> List[Dict]:
        """Get leaderboard data"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT u.username, 
                       COUNT(DISTINCT p.lesson_id) as lessons_completed,
                       AVG(p.score) as avg_score,
                       COUNT(b.badge_name) as badges_earned
                FROM users u
                LEFT JOIN progress p ON u.id = p.user_id AND p.completed = 1
                LEFT JOIN badges b ON u.id = b.user_id
                GROUP BY u.id
                ORDER BY lessons_completed DESC, avg_score DESC
                LIMIT 10
            ''')
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
