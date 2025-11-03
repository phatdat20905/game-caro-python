"""
Database connection and initialization
"""

import sqlite3
import os
from shared.utils import log, create_dirs_if_not_exists

class Database:
    """SQLite database manager"""
    
    def __init__(self, db_path="database/caro_game.db"):
        self.db_path = db_path
        self.connection = None
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure database directory and file exist"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            create_dirs_if_not_exists(db_dir)
    
    def connect(self):
        """Connect to database"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            log(f"Connected to database: {self.db_path}")
            return self.connection
        except sqlite3.Error as e:
            log(f"Database connection error: {e}", "ERROR")
            return None
    
    def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            self.connection.close()
            log("Disconnected from database")
    
    def get_connection(self):
        """Get database connection, create if not exists"""
        if self.connection is None:
            self.connect()
        return self.connection
    
    def init_database(self):
        """Initialize database with schema from SQL file"""
        conn = self.get_connection()
        if conn is None:
            log("Cannot initialize database: connection failed", "ERROR")
            return False
        
        try:
            # Read SQL file
            sql_file = "database/init_database.sql"
            if not os.path.exists(sql_file):
                log(f"SQL file not found: {sql_file}", "ERROR")
                return False
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Execute SQL script
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()
            log("Database initialized successfully")
            return True
        
        except sqlite3.Error as e:
            log(f"Database initialization error: {e}", "ERROR")
            return False
        except Exception as e:
            log(f"Error reading SQL file: {e}", "ERROR")
            return False
    
    def execute_query(self, query, params=None):
        """
        Execute a query (INSERT, UPDATE, DELETE)
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
        
        Returns:
            True if successful, False otherwise
        """
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as e:
            log(f"Query execution error: {e}", "ERROR")
            log(f"Query: {query}", "ERROR")
            return False
    
    def fetch_one(self, query, params=None):
        """
        Fetch one result
        
        Args:
            query: SQL query string
            params: Query parameters
        
        Returns:
            Single row result or None
        """
        conn = self.get_connection()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as e:
            log(f"Fetch one error: {e}", "ERROR")
            return None
    
    def fetch_all(self, query, params=None):
        """
        Fetch all results
        
        Args:
            query: SQL query string
            params: Query parameters
        
        Returns:
            List of rows or empty list
        """
        conn = self.get_connection()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            log(f"Fetch all error: {e}", "ERROR")
            return []
    
    def get_last_insert_id(self):
        """Get last inserted row ID"""
        conn = self.get_connection()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            return cursor.lastrowid
        except sqlite3.Error as e:
            log(f"Get last insert ID error: {e}", "ERROR")
            return None


# Global database instance
_db_instance = None

def get_database():
    """Get global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
