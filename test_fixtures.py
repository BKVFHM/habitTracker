"""
Test fixtures with predefined habits and 4 weeks of sample data.
"""
from datetime import datetime, timedelta
from habit import Habit, Periodicity
from database import HabitDatabase


def create_test_fixtures() -> None:
    """Create 5 predefined habits with 4 weeks of sample tracking data."""
    db = HabitDatabase()
    
    # Base date - 4 weeks ago
    base_date = datetime.now() - timedelta(weeks=4)
    
    # Habit 1: Daily - Drink Water (very consistent)
    drink_water = Habit("Drink 8 glasses of water", Periodicity.DAILY, base_date)
    for day in range(28):  # 4 weeks
        if day not in [5, 12, 19]:  # Miss 3 days
            completion_date = base_date + timedelta(days=day, hours=10)
            drink_water.complete_task(completion_date)
    
    # Habit 2: Daily - Exercise (moderately consistent)
    exercise = Habit("Exercise for 30 minutes", Periodicity.DAILY, base_date + timedelta(days=1))
    for day in range(27):  # Started 1 day later
        if day % 3 != 0:  # Miss every 3rd day
            completion_date = base_date + timedelta(days=day+1, hours=18)
            exercise.complete_task(completion_date)
    
    # Habit 3: Daily - Read (inconsistent)
    read = Habit("Read for 20 minutes", Periodicity.DAILY, base_date + timedelta(days=2))
    for day in [0, 1, 3, 4, 7, 8, 9, 14, 15, 21, 22, 23, 24]:  # Sporadic completions
        completion_date = base_date + timedelta(days=day+2, hours=20)
        read.complete_task(completion_date)
    
    # Habit 4: Weekly - Clean House (consistent)
    clean_house = Habit("Deep clean the house", Periodicity.WEEKLY, base_date)
    for week in range(4):  # All 4 weeks
        completion_date = base_date + timedelta(weeks=week, days=6, hours=14)  # Saturdays
        clean_house.complete_task(completion_date)
    
    # Habit 5: Weekly - Grocery Shopping (missed one week)
    grocery_shopping = Habit("Weekly grocery shopping", Periodicity.WEEKLY, base_date + timedelta(days=3))
    for week in [0, 1, 3]:  # Miss week 2
        completion_date = base_date + timedelta(weeks=week, days=3+7, hours=11)  # Sundays
        grocery_shopping.complete_task(completion_date)
    
    # Save all habits to database
    habits = [drink_water, exercise, read, clean_house, grocery_shopping]
    for habit in habits:
        db.save_habit(habit)
    
    print("Test fixtures created successfully!")
    print(f"Created {len(habits)} habits with sample data:")
    for habit in habits:
        print(f"  - {habit.name} ({habit.periodicity.value}): {len(habit.completions)} completions")


if __name__ == "__main__":
    create_test_fixtures()