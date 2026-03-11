"""
Analytics module using functional programming paradigm for habit analysis.
"""
from typing import List, Callable, Optional
from functools import reduce
from habit import Habit, Periodicity


def get_all_habits(habits: List[Habit]) -> List[str]:
    """
    Return a list of all currently tracked habits.
    
    Args:
        habits: List of all habits
        
    Returns:
        List of habit names
    """
    return list(map(lambda h: h.name, habits))


def get_habits_by_periodicity(habits: List[Habit], periodicity: Periodicity) -> List[str]:
    """
    Return a list of all habits with the same periodicity.
    
    Args:
        habits: List of all habits
        periodicity: The periodicity to filter by
        
    Returns:
        List of habit names with matching periodicity
    """
    filtered_habits = filter(lambda h: h.periodicity == periodicity, habits)
    return list(map(lambda h: h.name, filtered_habits))


def get_longest_streak_all_habits(habits: List[Habit]) -> int:
    """
    Return the longest run streak of all defined habits.
    
    Args:
        habits: List of all habits
        
    Returns:
        The longest streak across all habits
    """
    if not habits:
        return 0
    
    streaks = map(lambda h: h.get_longest_streak(), habits)
    return reduce(max, streaks, 0)


def get_longest_streak_for_habit(habits: List[Habit], habit_name: str) -> int:
    """
    Return the longest run streak for a given habit.
    
    Args:
        habits: List of all habits
        habit_name: Name of the habit to analyze
        
    Returns:
        The longest streak for the specified habit, or 0 if not found
    """
    habit_filter: Callable[[Habit], bool] = lambda h: h.name == habit_name
    matching_habits = list(filter(habit_filter, habits))
    
    if not matching_habits:
        return 0
    
    return matching_habits[0].get_longest_streak()


def get_current_streaks(habits: List[Habit]) -> List[tuple]:
    """
    Get current streaks for all habits.
    
    Args:
        habits: List of all habits
        
    Returns:
        List of tuples (habit_name, current_streak)
    """
    return list(map(lambda h: (h.name, h.get_current_streak()), habits))


def get_habits_with_no_completions(habits: List[Habit]) -> List[str]:
    """
    Get habits that have never been completed.
    
    Args:
        habits: List of all habits
        
    Returns:
        List of habit names with no completions
    """
    no_completion_filter: Callable[[Habit], bool] = lambda h: len(h.completions) == 0
    filtered_habits = filter(no_completion_filter, habits)
    return list(map(lambda h: h.name, filtered_habits))


def get_most_completed_habit(habits: List[Habit]) -> Optional[str]:
    """
    Get the habit with the most completions.
    
    Args:
        habits: List of all habits
        
    Returns:
        Name of the most completed habit, or None if no habits exist
    """
    if not habits:
        return None
    
    completion_counts = map(lambda h: (h.name, len(h.completions)), habits)
    most_completed = reduce(
        lambda a, b: a if a[1] >= b[1] else b,
        completion_counts
    )
    
    return most_completed[0] if most_completed[1] > 0 else None