import cv2

class CameraManager:
    def __init__(self, cam_id=0, width=960, height=720):
        self.cam_id = cam_id
        self.WIDTH = width
        self.HEIGHT = height
        self.vid = None

    def start_cam(self):
        # Initialises the camera
        self.vid = cv2.VideoCapture(self.cam_id)
        self.vid.set(3, self.WIDTH)
        self.vid.set(4,self.HEIGHT)

    def get_frame(self):
        if self.vid is None:
            return None
        ret, frame = self.vid.read()
        if not ret:
            return None
        return cv2.flip(frame, 1)

    def stop(self):
        if self.vid:
            self.vid.release()
            self.vid = None