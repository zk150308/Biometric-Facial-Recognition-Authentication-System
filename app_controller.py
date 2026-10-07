# Import classes from files
from camera_manager import CameraManager
from face_recognition_class import FaceRecognition
from data_manager import DataManager
from auth_service import AuthService
from encryption_manager import EncryptionManager
from session_manager import SessionManager

class AppController:
    def __init__(self):
        self.camera = CameraManager()
        self.face_recognition = FaceRecognition()
        self.encryption = EncryptionManager()
        self.data_manager = DataManager()
        self.auth_service = AuthService(self.data_manager, self.encryption)
        self.session_manager = SessionManager(timeout_seconds=900) # 120s for testing

    # Camera
    def start_camera(self):
        self.camera.start_cam()

    def stop_camera(self):
        self.camera.stop()

    def get_frame(self):
        return self.camera.get_frame()

    # Login
    def login_with_frame(self, frame):
        embedding = self.face_recognition.extract_embedding(frame)
        if embedding is None:
            return None 
        user = self.auth_service.authenticate(embedding)
        if user:
            self.session_manager.start_session(user["id"]) 
            return user

    def signup_with_frame(self, frame, name):
        embedding = self.face_recognition.extract_embedding(frame)
        if embedding is None:
            return "invalid"
        if self.auth_service.face_exists(embedding):
            return "exists"
        encrypted = self.encryption.encrypt_embedding(embedding)
        user_id = self.data_manager.add_user(name, encrypted)
        self.session_manager.start_session(user_id)
        print(embedding)
        return "success"

    def check_session(self):
        if self.session_manager.has_timed_out():
            self.logout()
            return False
        return True

    def logout(self):
        self.session_manager.logout()