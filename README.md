# Biometric Facial Recognition Authentication System

An end-to-end biometric authentication pipeline and GUI that processes real-time video feeds at 30+ FPS, replacing traditional password-based authentication with facial feature extraction. 

## Performance & Architecture

* **High-Accuracy Deep Metric Learning:** Utilizes a ResNet-based Convolutional Neural Network (CNN) to generate 128-dimensional facial embedding vectors.
* **Low-Latency Verification:** Achieves sub-100ms verification latency during live camera feed processing.
* **Benchmark Accuracy:** Built upon `dlib`'s state-of-the-art face recognition model, achieving 99.38% accuracy on the standard Labeled Faces in the Wild (LFW) dataset.
* **Modular Object-Oriented Design:** The system is heavily decoupled, separating the camera stream handling (`CameraManager`), authentication logic (`AuthService`), biometric extraction (`FaceRecognition`), and UI state (`UIController`).
* **Encrypted Storage:** Raw biometric data is never stored; embedding vectors are encrypted and written to local JSON storage alongside unique user IDs.

## Tech Stack
* **Python 3.12**
* **OpenCV:** Real-time camera feed capture, frame flip, and BGR-to-RGB conversion.
* **dlib / face_recognition:** 68-point facial landmark alignment and 128D vector embedding generation.
* **NumPy:** High-performance matrix operations and array handling for embedding comparisons.
* **Tkinter & Pillow:** Event-driven graphical user interface and drawing canvas.

## System Workflow

1. **Capture & Pre-Processing:** Extracts frames from the webcam using OpenCV, converting them to RGB and applying alignment.
2. **Detection & Embedding:** `dlib` extracts 68 facial landmarks to isolate the face, passing the cropped region through the CNN to output a 128D numeric vector.
3. **Authentication:** The `AuthService` computes the Euclidean distance between the live vector and securely stored vectors. A threshold of 0.6 determines a verified match.
4. **Session Management:** The `SessionManager` handles secure login states and automatically expires idle sessions after a set timeout.

## Quick Start

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt