"""
Main entry point for the Habit Tracker application.
"""
from cli import HabitTrackerCLI

if __name__ == "__main__":
    app = HabitTrackerCLI()
    app.run()