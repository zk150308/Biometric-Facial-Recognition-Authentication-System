import tkinter as tk
from frames import HomeFrame, LoginFrame, SignupFrame, DashboardFrame, DrawingFrame

class UIController(tk.Tk):
    def __init__(self, app_controller):
        super().__init__() # Creates the window
        self.app = app_controller
        self.title("Face Recognition Program")
        self.geometry("800x600")
        self.frames = {}

        # Each frame now needs to be created
        for frameClass in (HomeFrame, LoginFrame, SignupFrame, DashboardFrame, DrawingFrame):
            frame = frameClass(self)
            self.frames[frameClass] = frame
            frame.place(relwidth=1, relheight=1)

        # Frame Timeout
        self.after(1000, self.check_session)

        # Displays home frame when starting
        self.show_frame(HomeFrame)

    def show_frame(self, frame_class):
        self.app.session_manager.update_activity()

        # Stop camera streams
        self.frames[LoginFrame].stop_stream()
        self.frames[SignupFrame].stop_stream()
        self.app.stop_camera() 

        # Refresh dashboard drawings when showing it
        if frame_class == DashboardFrame:
            self.frames[DashboardFrame].refresh_drawings()

        # Prepare drawing canvas when entering drawing frame
        if frame_class == DrawingFrame:
            self.frames[DrawingFrame].clear_canvas()
            self.frames[DrawingFrame].load_canvas()

        # Show frame
        self.frames[frame_class].tkraise()

        # Start camera for login/signup
        if frame_class in (LoginFrame, SignupFrame):
            self.app.start_camera()
            self.frames[frame_class].start_stream()

    def check_session(self):
        # Timer which runs every second
        if self.app.session_manager.is_logged_in():
            if self.app.session_manager.has_timed_out():
                self.app.logout()
                self.show_frame(HomeFrame)
        self.after(1000, self.check_session)