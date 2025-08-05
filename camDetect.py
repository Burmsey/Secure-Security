def init(value, should_close=None):
    import cv2
    import time
    import os
    import datetime

    print("Initializing camera with value:", value)
    cap = cv2.VideoCapture(value)
    if not cap.isOpened():
        print(f"Camera at index {value} could not be opened.")
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

    cv2.namedWindow("Camera")
    cv2.setMouseCallback("Camera", on_mouse)

    while True:
        d, frame = cap.read()
        if not d or frame is None:
            print("Failed to read from camera. Exiting...")
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
                print("Capturing...")
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
                    print('Recording ended.')
                    print("Saved to:", os.getcwd(), filename)

        if detection:
            out.write(frame)

        for (x, y, width, height) in bodies:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)

        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        cv2.imshow("Camera", frame)

        if clicked[0]:
            print("Window clicked. Stopping camera...")
            break

        # Or if 's' key is pressed
        if cv2.waitKey(1) == ord('s'):
            print("Stopping camera...")
            break

    if detection:
        out.release()

    cap.release()
    cv2.destroyAllWindows()
