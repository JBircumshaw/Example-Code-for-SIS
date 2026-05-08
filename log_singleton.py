"""
log_singleton.py
----------------
Implements the Singleton design pattern for the centralised system Log.
Maps to the Singleton Pattern diagram in the SDS (Fig. 5) and supports
SRS requirements RE-15 (transaction logging) and RE-16 (search/inquiry
logging).

Only one Log instance can ever exist at runtime, ensuring all classes
write to the same central audit trail.
"""

import datetime


class Log:
    """Centralised system Log implemented as a Singleton."""

    _instance = None  # Stores the single shared instance for the lifetime of the program

    def __new__(cls):
        """Return the single shared instance, creating it on first call."""
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Guarded so that multiple Log() calls do not reset the entries list
        if not hasattr(self, "logs"):
            self.logs = []

    def create_log(self, action_type: str, details: str) -> None:
        """Append a new entry to the central audit log."""
        if not action_type:
            raise ValueError("action_type cannot be empty.")
        try:
            entry = {
                "action_type": action_type,
                "details": details,
                "timestamp": datetime.datetime.now()
            }
            self.logs.append(entry)
        except Exception as e:
            # Defensive: prevent logging failures from crashing the caller
            print(f"[Log] Failed to write entry: {e}")

    def view_logs(self) -> list:
        """Return all stored log entries."""
        return self.logs

    def clear(self) -> None:
        """Reset the log - used by tests to ensure isolation between cases."""
        self.logs = []
