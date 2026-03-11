# Habit Tracker

A Python-based habit tracking application that helps users create, track, and analyze their daily and weekly habits.

## Features

- **Habit Management**: Create, complete, and delete habits with daily or weekly periodicity
- **Streak Tracking**: Automatic calculation of current and longest streaks
- **Analytics**: Comprehensive analysis using functional programming paradigms
- **Data Persistence**: SQLite database for reliable data storage
- **CLI Interface**: User-friendly command-line interface
- **Test Fixtures**: Pre-loaded sample data for testing and demonstration

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

## Usage

### Running the Application
Start the habit tracker with:
```cmd
python cli.py
```

### Main Menu Options
1. **Create new habit** - Add a new daily or weekly habit
2. **Complete habit task** - Mark a habit as completed for today
3. **View all habits** - See all habits with their streaks and statistics
4. **View habits by periodicity** - Filter habits by daily or weekly
5. **View analytics** - Access detailed analytics and insights
6. **Delete habit** - Remove a habit from tracking
7. **Load test fixtures** - Load 5 predefined habits with sample data
8. **Exit** - Close the application

### Creating a New Habit
1. Select option 1 from the main menu
2. Enter a descriptive name for your habit
3. Choose periodicity:
   - Daily: Must be completed every day
   - Weekly: Must be completed once per week

### Completing a Habit
1. Select option 2 from the main menu
2. Choose the habit you want to mark as completed
3. The completion will be recorded with the current timestamp

### Analytics Features
The analytics module provides insights using functional programming:
- List all tracked habits
- Filter habits by periodicity (daily/weekly)
- Find longest streak across all habits
- Get longest streak for a specific habit
- View current streaks for all habits
- Identify habits with no completions
- Find the most completed habit

## Test Fixtures

The application comes with 5 predefined habits and 4 weeks of sample data:

1. **"Drink 8 glasses of water"** (Daily) - Very consistent, missed 3 days
2. **"Exercise for 30 minutes"** (Daily) - Moderately consistent, missed every 3rd day
3. **"Read for 20 minutes"** (Daily) - Inconsistent, sporadic completions
4. **"Deep clean the house"** (Weekly) - Consistent, completed all 4 weeks
5. **"Weekly grocery shopping"** (Weekly) - Missed one week out of four

To load test fixtures:
1. Run the application: `python cli.py`
2. Select option 7 from the main menu
3. Or run directly: `python test_fixtures.py`

## Running Tests

Execute the unit test suite:
```cmd
python test_habit_tracker.py
```

The test suite covers:
- Habit creation and task completion
- Streak calculations for daily and weekly habits
- Database operations (save, load, delete)
- Analytics functions
- Edge cases and error handling

## Architecture

### Object-Oriented Design
- **Habit Class**: Encapsulates habit data and behavior
- **Periodicity Enum**: Defines habit frequencies (DAILY, WEEKLY)
- **HabitDatabase Class**: Handles data persistence

### Functional Programming
The analytics module uses functional programming paradigms:
- `map()` for transformations
- `filter()` for data filtering
- `reduce()` for aggregations
- Lambda functions for concise operations

### Data Persistence
- SQLite database with two tables: `habits` and `completions`
- Automatic database initialization
- Foreign key relationships for data integrity

## Streak Calculation Logic

### Daily Habits
- A streak is broken if a day is missed
- Current streak counts consecutive days from today backwards
- Longest streak finds the maximum consecutive days ever achieved

### Weekly Habits
- A streak is broken if a week is missed
- Weeks start on Monday (ISO standard)
- Current streak counts consecutive weeks from current week backwards

## Error Handling

The application includes comprehensive error handling:
- Input validation for user entries
- Database connection error handling
- Graceful handling of missing or invalid data
- User-friendly error messages

## Future Enhancements

Potential improvements for future versions:
- Web interface using Flask or Django
- Data export/import functionality
- Habit categories and tags
- Reminder notifications
- Progress visualization
- Multi-user support
