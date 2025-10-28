import sqlite3
import pandas as pd
from datetime import datetime
import os

class Database:
    """Database handler for storing trading recommendations"""
    
    def __init__(self, db_path='trading_recommendations.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                symbol TEXT NOT NULL,
                signal TEXT NOT NULL,
                entry_price REAL NOT NULL,
                target_3 REAL,
                target_5 REAL,
                target_10 REAL,
                stop_loss REAL,
                confidence REAL,
                indicators TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_recommendation(self, symbol, signal, entry_price, target_3, target_5, 
                          target_10, stop_loss, confidence, indicators):
        """Add a new recommendation to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recommendations 
            (symbol, signal, entry_price, target_3, target_5, target_10, 
             stop_loss, confidence, indicators)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (symbol, signal, entry_price, target_3, target_5, target_10, 
              stop_loss, confidence, indicators))
        
        conn.commit()
        
        # Keep only last 100 recommendations
        cursor.execute('''
            DELETE FROM recommendations 
            WHERE id NOT IN (
                SELECT id FROM recommendations 
                ORDER BY timestamp DESC 
                LIMIT 100
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_recent_recommendations(self, limit=10):
        """Get recent recommendations from database"""
        conn = sqlite3.connect(self.db_path)
        
        query = f'''
            SELECT * FROM recommendations 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_recommendations_by_symbol(self, symbol, limit=20):
        """Get recommendations for a specific symbol"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM recommendations 
            WHERE symbol = ?
            ORDER BY timestamp DESC 
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=(symbol, limit))
        conn.close()
        
        return df
    
    def get_all_recommendations(self):
        """Get all recommendations"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM recommendations ORDER BY timestamp DESC', conn)
        conn.close()
        return df
    
    def clear_old_recommendations(self, days=30):
        """Clear recommendations older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM recommendations 
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Get statistics about recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total recommendations
        cursor.execute('SELECT COUNT(*) FROM recommendations')
        stats['total'] = cursor.fetchone()[0]
        
        # Buy/Sell/Hold counts
        cursor.execute('SELECT signal, COUNT(*) FROM recommendations GROUP BY signal')
        signal_counts = cursor.fetchall()
        stats['signals'] = {signal: count for signal, count in signal_counts}
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) FROM recommendations')
        stats['avg_confidence'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
