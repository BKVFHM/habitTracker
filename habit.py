"""
Core habit tracking classes for the habit tracker application.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


class Periodicity(Enum):
    """Enum for habit periodicity types."""
    DAILY = "daily"
    WEEKLY = "weekly"


class Habit:
    """
    Represents a habit with task specification and periodicity.
    
    Attributes:
        name: The name/description of the habit
        periodicity: How often the habit should be completed (daily/weekly)
        created_date: When the habit was created
        completions: List of completion timestamps
    """
    
    def __init__(self, name: str, periodicity: Periodicity, created_date: Optional[datetime] = None):
        """
        Initialize a new habit.
        
        Args:
            name: The habit name/description
            periodicity: How often the habit should be completed
            created_date: When the habit was created (defaults to now)
        """
        self.name = name
        self.periodicity = periodicity
        self.created_date = created_date or datetime.now()
        self.completions: List[datetime] = []
    
    def complete_task(self, completion_date: Optional[datetime] = None) -> None:
        """
        Mark the habit as completed for a given date.
        
        Args:
            completion_date: When the task was completed (defaults to now)
        """
        completion_date = completion_date or datetime.now()
        self.completions.append(completion_date)
        self.completions.sort()  # Keep completions sorted
    
    def get_current_streak(self) -> int:
        """
        Calculate the current streak of consecutive completions.
        
        Returns:
            The number of consecutive periods completed
        """
        if not self.completions:
            return 0
        
        # Get period length in days
        period_days = 1 if self.periodicity == Periodicity.DAILY else 7
        
        # Start from the most recent completion and work backwards
        current_date = datetime.now().date()
        streak = 0
        
        # Group completions by period
        periods_completed = set()
        for completion in self.completions:
            if self.periodicity == Periodicity.DAILY:
                periods_completed.add(completion.date())
            else:  # Weekly
                # Get the start of the week (Monday)
                week_start = completion.date() - timedelta(days=completion.weekday())
                periods_completed.add(week_start)
        
        # Check consecutive periods backwards from current period
        check_date = current_date
        if self.periodicity == Periodicity.WEEKLY:
            check_date = current_date - timedelta(days=current_date.weekday())
        
        while True:
            if check_date in periods_completed:
                streak += 1
                check_date -= timedelta(days=period_days)
            else:
                break
        
        return streak
    
    def get_longest_streak(self) -> int:
        """
        Calculate the longest streak ever achieved for this habit.
        
        Returns:
            The longest number of consecutive periods completed
        """
        if not self.completions:
            return 0
        
        # Group completions by period
        periods_completed = set()
        for completion in self.completions:
            if self.periodicity == Periodicity.DAILY:
                periods_completed.add(completion.date())
            else:  # Weekly
                week_start = completion.date() - timedelta(days=completion.weekday())
                periods_completed.add(week_start)
        
        if not periods_completed:
            return 0
        
        # Sort periods and find longest consecutive sequence
        sorted_periods = sorted(periods_completed)
        max_streak = 1
        current_streak = 1
        period_days = 1 if self.periodicity == Periodicity.DAILY else 7
        
        for i in range(1, len(sorted_periods)):
            expected_next = sorted_periods[i-1] + timedelta(days=period_days)
            if sorted_periods[i] == expected_next:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak