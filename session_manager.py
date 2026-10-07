import time
from session import Session

class SessionManager:
    def __init__(self, timeout_seconds):
        self.timeout = timeout_seconds
        self.current_session = None

    def start_session(self, user_id):
        # Create session
        self.current_session = Session(user_id)

    def is_logged_in(self):
        # Returns true if there is a value
        return self.current_session is not None

    def get_user_id(self):
        # If there is a session return the ID
        if self.current_session:
            return self.current_session.user_id
        return None

    def update_activity(self):
        # Called when something happens
        if self.current_session:
            self.current_session.update_activity()

    def has_timed_out(self):
        if not self.current_session:
            return False
        # Calculates inactive time
        inactive_time = time.time() - self.current_session.last_activity
        return inactive_time > self.timeout 

    def logout(self):
        self.current_session = None