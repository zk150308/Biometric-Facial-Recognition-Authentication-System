import json
import os

class DataManager:
    def __init__(self, filename = "users.json"):
        self.filename = filename
        self.users = []
        self.next_id = 1
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r") as f:
            data = json.load(f)
            self.users = data.get("users", []) # Empty list if no values
            self.next_id = data.get("next_id", 1) # 1 if no values

    def save(self):
        with open(self.filename, "w") as f:
            json.dump({
                "next_id" : self.next_id,
                "users" : self.users
            }, f, indent=1) # Data, Output file, Indent

    def add_user(self, name, encrypted_embedding):
        # User structure
        user = {
            "id" : self.next_id,
            "name" : name,
            "embedding" : encrypted_embedding.tolist() # Converts the array to a list
        }
        self.users.append(user)
        self.next_id += 1
        self.save()
        return user["id"]

    def get_users(self):
        return self.users