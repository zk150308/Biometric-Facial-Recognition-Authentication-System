import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk, ImageGrab
import os

class HomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Title label
        tk.Label(
            self,
            text="Altrincham Grammar School for Boys",
            font=("Arial", 24)
        ).pack(pady=40)

        # Login button goes to LoginFrame
        tk.Button(
            self,
            text="Log in",
            width=20,
            command=lambda: master.show_frame(LoginFrame)
        ).pack(pady=10)

        # Signup button goes to SignupFrame
        tk.Button(
            self,
            text="Sign up",
            width=20,
            command=lambda: master.show_frame(SignupFrame)
        ).pack(pady=10)

        # Quit button closes program 
        tk.Button(
            self,
            text="Quit",
            width=20,
            command=master.destroy
        ).pack(pady=10)

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Title
        tk.Label(
            self,
            text="Login",
            font=("Arial", 24)
        ).pack(pady=20)

        # Placeholder for camera feed
        self.camera_label = tk.Label(
            self,
            text="Camera Feed",
            width=640,
            height=480,
            bg="grey"
        )
        self.camera_label.pack(pady=10)

        # Status messages (success/error)
        self.status_label = tk.Label(
            self,
            text="",
            fg="red"
        )
        self.status_label.pack(pady=5) 

        # Authenticate button
        tk.Button(
            self,
            text="Authenticate",
            width=20,
            command=self.authenticate
        ).pack(pady=10)

        # Back button returns to HomeFrame
        tk.Button(
            self,
            text="Back",
            width=20,
            command=lambda: master.show_frame(HomeFrame)
        ).pack(pady=10)

    def start_stream(self):
        self.streaming = True
        self.update_frame()

    def update_frame(self):
        if not self.streaming:
            return
        frame = self.master.app.get_frame()
        if (
            frame is None
            or not hasattr(frame, "shape")
            or frame.size == 0
            or frame.dtype != "uint8"
        ):
            self.after(30, self.update_frame)
            return 
            
        faces = self.master.app.face_recognition.detect_faces(frame)
        frame_with_boxes = frame.copy()
        frame_with_boxes = self.master.app.face_recognition.draw_boxes(frame_with_boxes, faces)
        rgb = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img = img.resize((640, 480))
        imgtk = ImageTk.PhotoImage(img)
        self.camera_label.imgtk = imgtk
        self.camera_label.config(image=imgtk)
        self.after(30, self.update_frame)

    def authenticate(self):
        frame = self.master.app.get_frame() # Gets the latest frame
        if frame is None:
            self.status_label.config(
                text="Camera unavailable",
                fg="red"
            )
            return
            
        user = self.master.app.login_with_frame(frame) # App controller authenticates
        if user:
            self.status_label.config(
                text=f"{user['name']} successfully logged in.",
                fg="green"
            )
            self.master.app.session_manager.update_activity()
            self.master.show_frame(DashboardFrame) 
        else:
            self.status_label.config(
                text="Face not recognised",
                fg="red"
            )

    def stop_stream(self):
        self.streaming = False

class SignupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.streaming = False

        # Sign up
        tk.Label(
            self,
            text="Signup",
            font=("Arial", 24)
        ).pack(pady=20)

        self.camera_label = tk.Label(self, width=800, height=600)
        self.camera_label.pack(pady=10)
        
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)
        
        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.pack()

        tk.Button(
            self,
            text="Create Profile",
            command=self.create_profile 
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            command=lambda: master.show_frame(HomeFrame)
        ).pack(pady=10)

    def start_stream(self):
        self.streaming = True
        self.update_frame()

    def update_frame(self):
        if not self.streaming:
            return
        frame = self.master.app.get_frame()
        if (
            frame is None
            or not hasattr(frame, "shape")
            or frame.size == 0
            or frame.dtype != "uint8"
        ):
            self.after(30, self.update_frame)
            return

        faces = self.master.app.face_recognition.detect_faces(frame)
        frame_with_boxes = self.master.app.face_recognition.draw_boxes(frame, faces)
        rgb = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img = img.resize((640, 480))
        imgtk = ImageTk.PhotoImage(img) 
        self.camera_label.imgtk = imgtk
        self.camera_label.config(image=imgtk)
        self.after(30, self.update_frame)

    def create_profile(self):
        name = self.name_entry.get()
        frame = self.master.app.get_frame()
        result = self.master.app.signup_with_frame(frame, name)

        if result == "success":
            self.status_label.config(text="Profile created", fg="green")
            self.master.app.session_manager.update_activity()
            self.master.show_frame(DashboardFrame)
        elif result == "exists":
            self.status_label.config(text="Face already exists", fg="red")
        else:
            self.status_label.config(text="Invalid face", fg="red")

    def stop_stream(self):
        self.streaming = False

class DashboardFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.loaded_drawing = None

        tk.Label(
            self,
            text="Your Drawings",
            font=("Arial", 24) 
        ).pack(pady=30)

        self.cards_frame = tk.Frame(self)
        self.cards_frame.pack(pady=20)

        tk.Button(
            self,
            text="+ New Drawing",
            width=20,
            height=5,
            command=self.new_drawing
        ).pack(padx=10, pady=10)

        tk.Button(
            self,
            text="Logout",
            command=self.logout
        ).pack(pady=20) 

    def new_drawing(self):
        # Gets the user ID
        user_id = self.master.app.session_manager.get_user_id()
        if user_id is None:
            return

        # Checks and creates folder
        folder = f"drawings/user_{user_id}"
        if not os.path.exists(folder):
            count=0
        # Number of drawings
        else:
            count= len([f for f in os.listdir(folder) if f.endswith(".png")])

        if count >= 3:
            messagebox.showerror("Limit reached", "Maximum of 3 drawings allowed")
            return 

        # Start canvas
        self.set_drawing(None)
        self.master.show_frame(DrawingFrame)

    def logout(self):
        self.master.app.logout()
        self.master.show_frame(HomeFrame)

    def refresh_drawings(self):
        # Deletes all the buttons first
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Gets the user ID
        user_id = self.master.app.session_manager.get_user_id()
        if user_id is None:
            return

        # Checks for existing drawings to load
        folder = f"drawings/user_{user_id}"
        if not os.path.exists(folder):
            return

        # Creates a button for each image
        for filename in os.listdir(folder):
            # Ensures correct filetype
            if not filename.endswith(".png"):
                continue

            card = tk.Frame(self.cards_frame, relief="ridge", borderwidth=2)
            card.pack(padx=10, pady=10, fill="x")
            left = tk.Frame(card)
            left.pack(side="left", padx=10) 
            right = tk.Frame(card)
            right.pack(side="right", padx=10)

            tk.Button(
                left,
                text=filename,
                command=lambda f=filename: [self.set_drawing(f), self.master.show_frame(DrawingFrame)]
            ).pack()

            tk.Button(
                right,
                text="Delete",
                command=lambda f=filename: self.delete_drawing(f)
            ).pack()

    def delete_drawing(self, filename):
        user_id = self.master.app.session_manager.get_user_id()
        path = f"drawings/user_{user_id}/{filename}"
        if os.path.exists(path):
            os.remove(path)
        self.refresh_drawings()

    def set_drawing(self, pfilename):
        self.loaded_drawing = pfilename

    def get_drawing(self):
        return self.loaded_drawing

class DrawingFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.current_colour = "black" 
        self.brush_size = 4
        self.loaded_image = None # to keep reference to loaded PhotoImage

        # Title
        tk.Label(
            self,
            text="Drawing Pad",
            font=("Arial", 24)
        ).pack(pady=10)

        # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(pady=5)

        tk.Button(
            toolbar,
            text="Black",
            command=lambda: self.set_colour("black")
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Red",
            command=lambda: self.set_colour("red")
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Blue",
            command=lambda: self.set_colour("blue")
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Rubber",
            command=lambda: self.set_colour("white") 
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Save",
            command=self.save_drawing
        ).pack(side="left", padx=5)

        # Canvas
        self.canvas = tk.Canvas(
            self,
            bg="white",
            width=640,
            height=480
        )
        self.canvas.pack(pady=10)

        # Mouse binding
        self.canvas.bind("<B1-Motion>", self.draw)

        # Back Button
        tk.Button(
            self,
            text="Back to dashboard",
            width=25,
            command=lambda: master.show_frame(DashboardFrame)
        ).pack(pady=10)

    def set_colour(self, colour):
        self.current_colour = colour

    def draw(self, event):
        x, y = event.x, event.y
        r = self.brush_size
        self.canvas.create_oval( 
            x - r,
            y - r,
            x + r,
            y + r,
            fill=self.current_colour,
            outline=self.current_colour
        )

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_drawing(self):
        # Gets the user ID
        user_id = self.master.app.session_manager.get_user_id()
        if user_id is None:
            # No user logged in
            return

        # Ensures the folder exists
        folder = f"drawings/user_{user_id}"
        os.makedirs(folder, exist_ok=True)

        # Used to check if new drawing or existing one
        dashboard = self.master.frames[DashboardFrame]
        current_filename = dashboard.get_drawing()

        # Get all of the existing PNG drawings for this user
        existing = [f for f in os.listdir(folder) if f.endswith(".png")]

        # Updating Existing Users
        if current_filename is not None and current_filename in existing:
            path = os.path.join(folder, current_filename)
        # New drawing
        else:
            # Finds which IDs have already been used 
            used_numbers = []
            for f in existing: 
                number_part = f[len("drawing_") : -4] # Strips the drawing_ and .png parts
                n = int(number_part)
                used_numbers.append(n)

            # Finds the first free slot
            next_index = None
            for i in range(1,4):
                if i not in used_numbers:
                    next_index = i
                    break

            if next_index is None:
                # All slots are full
                messagebox.showerror("Limit reached", "Maximum of 3 drawings allowed")
                return

            filename = f"drawing_{next_index}.png"
            path = os.path.join(folder, filename)

        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, w, h))
        img.save(path, "PNG")
        dashboard.set_drawing(None)
        self.clear_canvas()
        self.master.show_frame(DashboardFrame) 

    def load_canvas(self):
        # Load the selected drawing to canvas
        filename = self.master.frames[DashboardFrame].get_drawing()

        # If none chosen, clear the canvas
        if filename is None:
            self.clear_canvas()
            return

        # Get ID and image path
        user_id = self.master.app.session_manager.get_user_id()
        folder = f"drawings/user_{user_id}"
        path = os.path.join(folder, filename)

        if not os.path.exists(path):
            self.clear_canvas()
            return

        self.clear_canvas()

        # Loads the image to the canvas
        img = Image.open(path)
        img = img.resize((640, 480))
        self.loaded_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.loaded_image)