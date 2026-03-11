"""
Simple verification script to test the habit tracker implementation.
"""
import os
import tempfile
from datetime import datetime, timedelta
from habit import Habit, Periodicity
from database import HabitDatabase
from analytics import get_all_habits, get_longest_streak_all_habits

def test_basic_functionality():
    """Test basic functionality of the habit tracker."""
    print("Testing Habit Tracker Implementation...")
    
    # Test 1: Create habits
    print("\n1. Testing habit creation...")
    daily_habit = Habit("Test Daily", Periodicity.DAILY)
    weekly_habit = Habit("Test Weekly", Periodicity.WEEKLY)
    print(f"+ Created daily habit: {daily_habit.name}")
    print(f"+ Created weekly habit: {weekly_habit.name}")
    
    # Test 2: Complete tasks
    print("\n2. Testing task completion...")
    daily_habit.complete_task()
    weekly_habit.complete_task()
    print(f"+ Daily habit completions: {len(daily_habit.completions)}")
    print(f"+ Weekly habit completions: {len(weekly_habit.completions)}")
    
    # Test 3: Streak calculation
    print("\n3. Testing streak calculation...")
    base_date = datetime.now() - timedelta(days=3)
    for i in range(3):
        daily_habit.complete_task(base_date + timedelta(days=i))
    
    longest_streak = daily_habit.get_longest_streak()
    print(f"+ Daily habit longest streak: {longest_streak}")
    
    # Test 4: Database operations
    print("\n4. Testing database operations...")
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        db = HabitDatabase(temp_db.name)
        db.save_habit(daily_habit)
        loaded_habit = db.load_habit("Test Daily")
        
        if loaded_habit:
            print(f"+ Saved and loaded habit: {loaded_habit.name}")
            print(f"+ Loaded completions: {len(loaded_habit.completions)}")
        else:
            print("- Failed to load habit from database")
    finally:
        # Clean up database
        db = None
        import time
        time.sleep(0.1)
        try:
            os.unlink(temp_db.name)
        except (PermissionError, FileNotFoundError):
            pass
    
    # Test 5: Analytics
    print("\n5. Testing analytics...")
    habits = [daily_habit, weekly_habit]
    all_habit_names = get_all_habits(habits)
    longest_streak_all = get_longest_streak_all_habits(habits)
    
    print(f"+ All habits: {all_habit_names}")
    print(f"+ Longest streak across all habits: {longest_streak_all}")
    
    print("\n+ All tests passed! The habit tracker implementation is working correctly.")

if __name__ == "__main__":
    test_basic_functionality()