class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "logs"):
            self.logs = []

    def create_log(self, action_type: str, details: str):
        self.logs.append({
            "action_type": action_type,
            "details": details
        })

    def view_logs(self):
        return self.logs