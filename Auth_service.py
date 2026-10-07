import face_recognition
import numpy as np

class AuthService:
    def __init__(self, data_manager, encryption_manager):
        self.encryption = encryption_manager
        self.data_manager = data_manager

    def authenticate(self, embedding):
        users = self.data_manager.get_users()
        for user in users:
            encrypted_embedding = np.array(user["embedding"])
            stored_embedding = self.encryption.decrypt_embedding(encrypted_embedding)
            if face_recognition.compare_faces([stored_embedding], embedding, tolerance=0.6)[0]:
                return user
        return None

    def face_exists(self, embedding):
        for user in self.data_manager.get_users():
            stored_encrypted = np.array(user["embedding"])
            stored_embedding = self.encryption.decrypt_embedding(stored_encrypted)
            if face_recognition.compare_faces([stored_embedding], embedding, tolerance=0.6)[0]:
                return True
        return False