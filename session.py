import time

class Session:
    def __init__(self, user_id):
        self.user_id = user_id
        self.start_time = time.time()
        self.last_activity = time.time()

    def update_activity(self):
        self.last_activity = time.time()