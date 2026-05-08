# Singleton pattern - only one Log instance can ever exist

class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "logs"):
            self.logs = []

    def create_log(self, action_type, details):
        self.logs.append({
            "action_type": action_type,
            "details": details
        })

    def view_logs(self):
        return self.logs

    def clear(self):
        self.logs = []
