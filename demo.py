"""
Demo script showing the habit tracker functionality with test fixtures.
"""
from test_fixtures import create_test_fixtures
from database import HabitDatabase
from analytics import (
    get_all_habits, get_habits_by_periodicity, get_longest_streak_all_habits,
    get_current_streaks, get_most_completed_habit
)
from habit import Periodicity

def run_demo():
    """Run a demonstration of the habit tracker features."""
    print("=== Habit Tracker Demo ===\n")
    
    # Create test fixtures
    print("1. Creating test fixtures with 5 habits and 4 weeks of data...")
    create_test_fixtures()
    
    # Load habits from database
    db = HabitDatabase()
    habits = db.load_all_habits()
    
    print(f"\n2. Loaded {len(habits)} habits from database:")
    for habit in habits:
        print(f"   • {habit.name} ({habit.periodicity.value})")
        print(f"     Completions: {len(habit.completions)}")
        print(f"     Current streak: {habit.get_current_streak()}")
        print(f"     Longest streak: {habit.get_longest_streak()}")
        print()
    
    # Analytics demonstration
    print("3. Analytics Results:")
    print("   a) All tracked habits:")
    all_habits = get_all_habits(habits)
    for name in all_habits:
        print(f"      - {name}")
    
    print("\n   b) Daily habits:")
    daily_habits = get_habits_by_periodicity(habits, Periodicity.DAILY)
    for name in daily_habits:
        print(f"      - {name}")
    
    print("\n   c) Weekly habits:")
    weekly_habits = get_habits_by_periodicity(habits, Periodicity.WEEKLY)
    for name in weekly_habits:
        print(f"      - {name}")
    
    print(f"\n   d) Longest streak across all habits: {get_longest_streak_all_habits(habits)} periods")
    
    print("\n   e) Current streaks:")
    current_streaks = get_current_streaks(habits)
    for name, streak in current_streaks:
        print(f"      - {name}: {streak} periods")
    
    most_completed = get_most_completed_habit(habits)
    print(f"\n   f) Most completed habit: {most_completed}")
    
    print("\n✅ Demo completed! You can now run 'python cli.py' to interact with the application.")

if __name__ == "__main__":
    run_demo()