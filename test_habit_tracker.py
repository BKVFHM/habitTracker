"""
Unit tests for the habit tracker application.
"""
import unittest
import os
import tempfile
from datetime import datetime, timedelta
from habit import Habit, Periodicity
from database import HabitDatabase
from analytics import (
    get_all_habits, get_habits_by_periodicity, get_longest_streak_all_habits,
    get_longest_streak_for_habit, get_current_streaks
)


class TestHabit(unittest.TestCase):
    """Test cases for the Habit class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.habit_daily = Habit("Test Daily", Periodicity.DAILY)
        self.habit_weekly = Habit("Test Weekly", Periodicity.WEEKLY)
    
    def test_habit_creation(self):
        """Test habit creation."""
        self.assertEqual(self.habit_daily.name, "Test Daily")
        self.assertEqual(self.habit_daily.periodicity, Periodicity.DAILY)
        self.assertIsInstance(self.habit_daily.created_date, datetime)
        self.assertEqual(len(self.habit_daily.completions), 0)
    
    def test_complete_task(self):
        """Test task completion."""
        initial_count = len(self.habit_daily.completions)
        self.habit_daily.complete_task()
        self.assertEqual(len(self.habit_daily.completions), initial_count + 1)
    
    def test_daily_streak_calculation(self):
        """Test streak calculation for daily habits."""
        base_date = datetime.now() - timedelta(days=5)
        
        # Complete for 3 consecutive days
        for i in range(3):
            self.habit_daily.complete_task(base_date + timedelta(days=i))
        
        # Current streak should be 0 (not current)
        self.assertEqual(self.habit_daily.get_current_streak(), 0)
        
        # Longest streak should be 3
        self.assertEqual(self.habit_daily.get_longest_streak(), 3)
    
    def test_weekly_streak_calculation(self):
        """Test streak calculation for weekly habits."""
        base_date = datetime.now() - timedelta(weeks=3)
        
        # Complete for 2 consecutive weeks
        for i in range(2):
            self.habit_weekly.complete_task(base_date + timedelta(weeks=i))
        
        self.assertEqual(self.habit_weekly.get_longest_streak(), 2)
    
    def test_empty_habit_streaks(self):
        """Test streak calculation for habits with no completions."""
        self.assertEqual(self.habit_daily.get_current_streak(), 0)
        self.assertEqual(self.habit_daily.get_longest_streak(), 0)


class TestDatabase(unittest.TestCase):
    """Test cases for the HabitDatabase class."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = HabitDatabase(self.temp_db.name)
        self.test_habit = Habit("Test Habit", Periodicity.DAILY)
    
    def tearDown(self):
        """Clean up test database."""
        # Close any remaining connections
        self.db = None
        # Small delay to ensure file is released
        import time
        time.sleep(0.1)
        try:
            os.unlink(self.temp_db.name)
        except (PermissionError, FileNotFoundError):
            # File might still be locked or already deleted
            pass
    
    def test_save_and_load_habit(self):
        """Test saving and loading habits."""
        # Add some completions
        self.test_habit.complete_task()
        self.test_habit.complete_task()
        
        # Save habit
        self.db.save_habit(self.test_habit)
        
        # Load habit
        loaded_habit = self.db.load_habit("Test Habit")
        
        self.assertIsNotNone(loaded_habit)
        self.assertEqual(loaded_habit.name, self.test_habit.name)
        self.assertEqual(loaded_habit.periodicity, self.test_habit.periodicity)
        self.assertEqual(len(loaded_habit.completions), 2)
    
    def test_load_nonexistent_habit(self):
        """Test loading a habit that doesn't exist."""
        result = self.db.load_habit("Nonexistent")
        self.assertIsNone(result)
    
    def test_load_all_habits(self):
        """Test loading all habits."""
        habit1 = Habit("Habit 1", Periodicity.DAILY)
        habit2 = Habit("Habit 2", Periodicity.WEEKLY)
        
        self.db.save_habit(habit1)
        self.db.save_habit(habit2)
        
        all_habits = self.db.load_all_habits()
        self.assertEqual(len(all_habits), 2)
        
        habit_names = [h.name for h in all_habits]
        self.assertIn("Habit 1", habit_names)
        self.assertIn("Habit 2", habit_names)
    
    def test_delete_habit(self):
        """Test deleting habits."""
        self.db.save_habit(self.test_habit)
        
        # Verify habit exists
        self.assertIsNotNone(self.db.load_habit("Test Habit"))
        
        # Delete habit
        result = self.db.delete_habit("Test Habit")
        self.assertTrue(result)
        
        # Verify habit is gone
        self.assertIsNone(self.db.load_habit("Test Habit"))
        
        # Try to delete nonexistent habit
        result = self.db.delete_habit("Nonexistent")
        self.assertFalse(result)


class TestAnalytics(unittest.TestCase):
    """Test cases for the analytics module."""
    
    def setUp(self):
        """Set up test habits."""
        self.habits = [
            Habit("Daily 1", Periodicity.DAILY),
            Habit("Daily 2", Periodicity.DAILY),
            Habit("Weekly 1", Periodicity.WEEKLY),
        ]
        
        # Add some completions
        base_date = datetime.now() - timedelta(days=10)
        for i in range(5):
            self.habits[0].complete_task(base_date + timedelta(days=i))
        
        for i in range(3):
            self.habits[1].complete_task(base_date + timedelta(days=i))
        
        self.habits[2].complete_task(base_date)
    
    def test_get_all_habits(self):
        """Test getting all habit names."""
        result = get_all_habits(self.habits)
        expected = ["Daily 1", "Daily 2", "Weekly 1"]
        self.assertEqual(sorted(result), sorted(expected))
    
    def test_get_habits_by_periodicity(self):
        """Test filtering habits by periodicity."""
        daily_habits = get_habits_by_periodicity(self.habits, Periodicity.DAILY)
        weekly_habits = get_habits_by_periodicity(self.habits, Periodicity.WEEKLY)
        
        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(len(weekly_habits), 1)
        self.assertIn("Daily 1", daily_habits)
        self.assertIn("Daily 2", daily_habits)
        self.assertIn("Weekly 1", weekly_habits)
    
    def test_get_longest_streak_all_habits(self):
        """Test getting longest streak across all habits."""
        result = get_longest_streak_all_habits(self.habits)
        self.assertGreaterEqual(result, 0)
    
    def test_get_longest_streak_for_habit(self):
        """Test getting longest streak for specific habit."""
        result = get_longest_streak_for_habit(self.habits, "Daily 1")
        self.assertGreaterEqual(result, 0)
        
        # Test nonexistent habit
        result = get_longest_streak_for_habit(self.habits, "Nonexistent")
        self.assertEqual(result, 0)
    
    def test_get_current_streaks(self):
        """Test getting current streaks for all habits."""
        result = get_current_streaks(self.habits)
        self.assertEqual(len(result), 3)
        
        # Each result should be a tuple (name, streak)
        for name, streak in result:
            self.assertIsInstance(name, str)
            self.assertIsInstance(streak, int)
            self.assertGreaterEqual(streak, 0)
    
    def test_empty_habits_list(self):
        """Test analytics functions with empty habits list."""
        empty_habits = []
        
        self.assertEqual(get_all_habits(empty_habits), [])
        self.assertEqual(get_habits_by_periodicity(empty_habits, Periodicity.DAILY), [])
        self.assertEqual(get_longest_streak_all_habits(empty_habits), 0)
        self.assertEqual(get_longest_streak_for_habit(empty_habits, "Any"), 0)
        self.assertEqual(get_current_streaks(empty_habits), [])


if __name__ == "__main__":
    unittest.main()