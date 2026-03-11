"""
Command Line Interface for the habit tracker application.
"""
import sys
from datetime import datetime
from habit import Habit, Periodicity
from database import HabitDatabase
from analytics import (
    get_all_habits, get_habits_by_periodicity, get_longest_streak_all_habits,
    get_longest_streak_for_habit, get_current_streaks, get_habits_with_no_completions,
    get_most_completed_habit
)
from test_fixtures import create_test_fixtures


class HabitTrackerCLI:
    """Command Line Interface for the habit tracker."""
    
    def __init__(self):
        """Initialize the CLI with database connection."""
        self.db = HabitDatabase()
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n=== Habit Tracker ===")
        print("1. Create new habit")
        print("2. Complete habit task")
        print("3. View all habits")
        print("4. View habits by periodicity")
        print("5. View analytics")
        print("6. Delete habit")
        print("7. Load test fixtures")
        print("8. Exit")
        print("=" * 21)
    
    def create_habit(self) -> None:
        """Create a new habit."""
        print("\n--- Create New Habit ---")
        name = input("Enter habit name: ").strip()
        
        if not name:
            print("Error: Habit name cannot be empty.")
            return
        
        # Check if habit already exists
        existing_habit = self.db.load_habit(name)
        if existing_habit:
            print(f"Error: Habit '{name}' already exists.")
            return
        
        print("Select periodicity:")
        print("1. Daily")
        print("2. Weekly")
        
        try:
            choice = int(input("Enter choice (1-2): "))
            if choice == 1:
                periodicity = Periodicity.DAILY
            elif choice == 2:
                periodicity = Periodicity.WEEKLY
            else:
                print("Error: Invalid choice.")
                return
        except ValueError:
            print("Error: Please enter a valid number.")
            return
        
        habit = Habit(name, periodicity)
        self.db.save_habit(habit)
        print(f"Habit '{name}' created successfully!")
    
    def complete_habit(self) -> None:
        """Mark a habit as completed."""
        print("\n--- Complete Habit Task ---")
        habits = self.db.load_all_habits()
        
        if not habits:
            print("No habits found. Create a habit first.")
            return
        
        print("Available habits:")
        for i, habit in enumerate(habits, 1):
            print(f"{i}. {habit.name} ({habit.periodicity.value})")
        
        try:
            choice = int(input("Select habit to complete (number): ")) - 1
            if 0 <= choice < len(habits):
                selected_habit = habits[choice]
                selected_habit.complete_task()
                self.db.save_habit(selected_habit)
                print(f"Completed '{selected_habit.name}' successfully!")
            else:
                print("Error: Invalid habit selection.")
        except ValueError:
            print("Error: Please enter a valid number.")
    
    def view_all_habits(self) -> None:
        """Display all habits with their current streaks."""
        print("\n--- All Habits ---")
        habits = self.db.load_all_habits()
        
        if not habits:
            print("No habits found.")
            return
        
        for habit in habits:
            current_streak = habit.get_current_streak()
            longest_streak = habit.get_longest_streak()
            print(f"• {habit.name}")
            print(f"  Periodicity: {habit.periodicity.value}")
            print(f"  Created: {habit.created_date.strftime('%Y-%m-%d')}")
            print(f"  Completions: {len(habit.completions)}")
            print(f"  Current streak: {current_streak}")
            print(f"  Longest streak: {longest_streak}")
            print()
    
    def view_habits_by_periodicity(self) -> None:
        """Display habits filtered by periodicity."""
        print("\n--- Habits by Periodicity ---")
        print("1. Daily habits")
        print("2. Weekly habits")
        
        try:
            choice = int(input("Enter choice (1-2): "))
            if choice == 1:
                periodicity = Periodicity.DAILY
            elif choice == 2:
                periodicity = Periodicity.WEEKLY
            else:
                print("Error: Invalid choice.")
                return
        except ValueError:
            print("Error: Please enter a valid number.")
            return
        
        habits = self.db.load_all_habits()
        filtered_habits = get_habits_by_periodicity(habits, periodicity)
        
        if not filtered_habits:
            print(f"No {periodicity.value} habits found.")
            return
        
        print(f"\n{periodicity.value.title()} habits:")
        for habit_name in filtered_habits:
            print(f"• {habit_name}")
    
    def view_analytics(self) -> None:
        """Display analytics menu and results."""
        print("\n--- Analytics ---")
        habits = self.db.load_all_habits()
        
        if not habits:
            print("No habits found for analysis.")
            return
        
        print("1. All tracked habits")
        print("2. Daily habits")
        print("3. Weekly habits")
        print("4. Longest streak (all habits)")
        print("5. Longest streak for specific habit")
        print("6. Current streaks")
        print("7. Habits with no completions")
        print("8. Most completed habit")
        
        try:
            choice = int(input("Enter choice (1-8): "))
            
            if choice == 1:
                habit_names = get_all_habits(habits)
                print(f"\nAll tracked habits ({len(habit_names)}):")
                for name in habit_names:
                    print(f"• {name}")
            
            elif choice == 2:
                daily_habits = get_habits_by_periodicity(habits, Periodicity.DAILY)
                print(f"\nDaily habits ({len(daily_habits)}):")
                for name in daily_habits:
                    print(f"• {name}")
            
            elif choice == 3:
                weekly_habits = get_habits_by_periodicity(habits, Periodicity.WEEKLY)
                print(f"\nWeekly habits ({len(weekly_habits)}):")
                for name in weekly_habits:
                    print(f"• {name}")
            
            elif choice == 4:
                longest_streak = get_longest_streak_all_habits(habits)
                print(f"\nLongest streak across all habits: {longest_streak} periods")
            
            elif choice == 5:
                habit_name = input("Enter habit name: ").strip()
                longest_streak = get_longest_streak_for_habit(habits, habit_name)
                if longest_streak > 0:
                    print(f"\nLongest streak for '{habit_name}': {longest_streak} periods")
                else:
                    print(f"\nHabit '{habit_name}' not found or has no completions.")
            
            elif choice == 6:
                current_streaks = get_current_streaks(habits)
                print("\nCurrent streaks:")
                for name, streak in current_streaks:
                    print(f"• {name}: {streak} periods")
            
            elif choice == 7:
                no_completion_habits = get_habits_with_no_completions(habits)
                if no_completion_habits:
                    print(f"\nHabits with no completions ({len(no_completion_habits)}):")
                    for name in no_completion_habits:
                        print(f"• {name}")
                else:
                    print("\nAll habits have at least one completion!")
            
            elif choice == 8:
                most_completed = get_most_completed_habit(habits)
                if most_completed:
                    print(f"\nMost completed habit: {most_completed}")
                else:
                    print("\nNo habits have been completed yet.")
            
            else:
                print("Error: Invalid choice.")
        
        except ValueError:
            print("Error: Please enter a valid number.")
    
    def delete_habit(self) -> None:
        """Delete a habit."""
        print("\n--- Delete Habit ---")
        habits = self.db.load_all_habits()
        
        if not habits:
            print("No habits found.")
            return
        
        print("Available habits:")
        for i, habit in enumerate(habits, 1):
            print(f"{i}. {habit.name}")
        
        try:
            choice = int(input("Select habit to delete (number): ")) - 1
            if 0 <= choice < len(habits):
                habit_name = habits[choice].name
                confirm = input(f"Are you sure you want to delete '{habit_name}'? (y/N): ")
                if confirm.lower() == 'y':
                    if self.db.delete_habit(habit_name):
                        print(f"Habit '{habit_name}' deleted successfully!")
                    else:
                        print("Error: Failed to delete habit.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Error: Invalid habit selection.")
        except ValueError:
            print("Error: Please enter a valid number.")
    
    def run(self) -> None:
        """Run the main CLI loop."""
        print("Welcome to the Habit Tracker!")
        
        while True:
            self.display_menu()
            
            try:
                choice = int(input("Enter your choice (1-8): "))
                
                if choice == 1:
                    self.create_habit()
                elif choice == 2:
                    self.complete_habit()
                elif choice == 3:
                    self.view_all_habits()
                elif choice == 4:
                    self.view_habits_by_periodicity()
                elif choice == 5:
                    self.view_analytics()
                elif choice == 6:
                    self.delete_habit()
                elif choice == 7:
                    create_test_fixtures()
                elif choice == 8:
                    print("Thank you for using Habit Tracker!")
                    sys.exit(0)
                else:
                    print("Error: Invalid choice. Please enter a number between 1-8.")
            
            except ValueError:
                print("Error: Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)


if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.run()