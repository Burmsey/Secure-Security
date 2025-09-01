import cv2
import os
import datetime
import time
import tkinter as tk
from tkinter import messagebox


def show_message(title, msg):
    root = tk.Tk()
    root.withdraw()  # hide the root window
    messagebox.showinfo(title, msg)
    root.destroy()


def init(value, should_close=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    cap = cv2.VideoCapture(value)

    # If this index doesn't work, try adjusting up or down
    if not cap.isOpened():
        show_message("Camera Error", f"Cam: {value + 1} could not be opened, this is likely due to Cam: {value + 1} not existing.")
        cap = cv2.VideoCapture(value - 1)
        if cap.isOpened():
            value = value - 1
            os.system('cls' if os.name == 'nt' else 'clear')
            show_message("Fallback", f"Using previous available camera [Cam: {value + 1}]")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            show_message("Camera Error", "No available cameras found near this index.")
            return

    current_time = datetime.datetime.now().strftime("DATE - %dth of the %m TIME %H-%M-%S")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")

    detection = False
    detection_stopped_time = None
    timer_started = False
    rec_delay = 5
    fps = 1.5

    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    clicked = [False]

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked[0] = True

    window_name = f"Cam: {value + 1}. [Click Window To Close]"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse)

    while True:
        d, frame = cap.read()
        if not d or frame is None:
            show_message("Camera Error", "Failed to read from camera. Exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 11)
        bodies = body_cascade.detectMultiScale(gray, 1.01, 6)

        if len(faces) + len(bodies) > 0:
            if not detection:
                detection = True
                timer_started = False
                filename = f"CAM_ALERT_{datetime.datetime.now().strftime('Year - %Y%m%d Time - %H%M%S')}.mp4"
                out = cv2.VideoWriter(filename, fourcc, fps, frame_size)
            else:
                timer_started = False

        else:
            if detection and not timer_started:
                timer_started = True
                detection_stopped_time = time.time()
            elif timer_started:
                if time.time() - detection_stopped_time >= rec_delay:
                    detection = False
                    timer_started = False
                    out.release()

        if detection:
            out.write(frame)

        for (x, y, width, height) in bodies:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)

        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        cv2.imshow(window_name, frame)

        if clicked[0]:
            break

    if detection:
        out.release()

    cap.release()
    cv2.destroyAllWindows()
