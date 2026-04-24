"""
Shared circuit breaker for remediation loop agents.
"""


def check(task_id, counts, limit=3):
    """Returns True if circuit is tripped (too many attempts)."""
    count = counts.get(task_id, 0) + 1
    counts[task_id] = count
    return count > limit


def reset(task_id, counts):
    """Clear the counter after a verified fix."""
    counts.pop(task_id, None)
