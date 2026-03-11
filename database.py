"""
Database module for persisting habit data using SQLite.
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from habit import Habit, Periodicity


class HabitDatabase:
    """Handles database operations for habit persistence."""
    
    def __init__(self, db_path: str = "habits.db"):
        """
        Initialize database connection and create tables if needed.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    periodicity TEXT NOT NULL,
                    created_date TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_date TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits (id)
                )
            """)
            conn.commit()
    
    def save_habit(self, habit: Habit) -> None:
        """
        Save a habit to the database.
        
        Args:
            habit: The habit to save
        """
        conn = sqlite3.connect(self.db_path)
        try:
            # Insert or update habit
            conn.execute("""
                INSERT OR REPLACE INTO habits (name, periodicity, created_date)
                VALUES (?, ?, ?)
            """, (habit.name, habit.periodicity.value, habit.created_date.isoformat()))
            
            # Get habit ID
            habit_id = conn.execute(
                "SELECT id FROM habits WHERE name = ?", (habit.name,)
            ).fetchone()[0]
            
            # Clear existing completions and insert new ones
            conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            
            for completion in habit.completions:
                conn.execute("""
                    INSERT INTO completions (habit_id, completion_date)
                    VALUES (?, ?)
                """, (habit_id, completion.isoformat()))
            
            conn.commit()
        finally:
            conn.close()
    
    def load_habit(self, name: str) -> Optional[Habit]:
        """
        Load a habit from the database by name.
        
        Args:
            name: The habit name
            
        Returns:
            The habit if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        try:
            habit_row = conn.execute("""
                SELECT name, periodicity, created_date FROM habits WHERE name = ?
            """, (name,)).fetchone()
            
            if not habit_row:
                return None
            
            habit = Habit(
                name=habit_row[0],
                periodicity=Periodicity(habit_row[1]),
                created_date=datetime.fromisoformat(habit_row[2])
            )
            
            # Load completions
            habit_id = conn.execute(
                "SELECT id FROM habits WHERE name = ?", (name,)
            ).fetchone()[0]
            
            completions = conn.execute("""
                SELECT completion_date FROM completions WHERE habit_id = ?
                ORDER BY completion_date
            """, (habit_id,)).fetchall()
            
            habit.completions = [datetime.fromisoformat(row[0]) for row in completions]
            
            return habit
        finally:
            conn.close()
    
    def load_all_habits(self) -> List[Habit]:
        """
        Load all habits from the database.
        
        Returns:
            List of all habits
        """
        conn = sqlite3.connect(self.db_path)
        try:
            habit_rows = conn.execute("""
                SELECT name, periodicity, created_date FROM habits
                ORDER BY created_date
            """).fetchall()
            
            habits = []
            for row in habit_rows:
                habit = Habit(
                    name=row[0],
                    periodicity=Periodicity(row[1]),
                    created_date=datetime.fromisoformat(row[2])
                )
                
                # Load completions
                habit_id = conn.execute(
                    "SELECT id FROM habits WHERE name = ?", (row[0],)
                ).fetchone()[0]
                
                completions = conn.execute("""
                    SELECT completion_date FROM completions WHERE habit_id = ?
                    ORDER BY completion_date
                """, (habit_id,)).fetchall()
                
                habit.completions = [datetime.fromisoformat(comp[0]) for comp in completions]
                habits.append(habit)
            
            return habits
        finally:
            conn.close()
    
    def delete_habit(self, name: str) -> bool:
        """
        Delete a habit from the database.
        
        Args:
            name: The habit name
            
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        try:
            # Get habit ID
            habit_row = conn.execute(
                "SELECT id FROM habits WHERE name = ?", (name,)
            ).fetchone()
            
            if not habit_row:
                return False
            
            habit_id = habit_row[0]
            
            # Delete completions first (foreign key constraint)
            conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            
            # Delete habit
            conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            conn.commit()
            
            return True
        finally:
            conn.close()