import cv2
import dlib
import face_recognition
import numpy as np

class FaceRecognition:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def detect_faces(self, frame):
        if frame is None:
            return []
        if len(frame.shape) == 3:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = np.ascontiguousarray(rgb, dtype=np.uint8)
            return self.detector(rgb)
        return self.detector(frame)

    def draw_boxes(self, frame, faces):
        for f in faces:
            x,y,w,h = f.left(), f.top(), f.width(), f.height()
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        return frame

    def extract_embedding(self, frame):
        if frame is None:
            return None
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self.detect_faces(frame) 
        if len(faces) != 1:
            return None
        f = faces[0]
        encodings = face_recognition.face_encodings(rgb, [(f.top(), f.right(), f.bottom(), f.left())])
        if not encodings:
            return None
        return encodings[0]