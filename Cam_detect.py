# import cv2
# import time
# import datetime
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import dotenv_values
# from Email_sender import message_mail

# secrets = dotenv_values(".env")

# sender_email = secrets["EMAIL"]
# receiver_email = secrets["RECIEVER"]
# password = secrets["PASSWORD"]
# subject = secrets["SUBJECT"]

# cap = cv2.VideoCapture(0)
# current_time = datetime.datetime.now().strftime("DATE: %d/%m TIME %H:%M:%S")

# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# body_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_fullbody.xml")
# eyes_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_eye.xml")

# detection = False
# detection_stopped_time = None
# timer_started = False
# rec_delay = 5

# frame_size = (int(cap.get(3)), int(cap.get(4)))
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# while True:
#     d, frame = cap.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 3, 3)
#     bodies = body_cascade.detectMultiScale(gray, 1.01, 6)
#     eyes = eyes_cascade.detectMultiScale(gray, 1.2, 3)

#     if len(faces) + len(bodies) + len(eyes)> 0:
#         if detection:
#             timer_started = False
#         else:
#             detection = True
#             out = cv2.VideoWriter(
#                 f"CAM_ALERT_{current_time}.mp4", fourcc, 40, frame_size)
#             print("Capturing...")
#     elif detection:
#         if timer_started:
#             if time.time() - detection_stopped_time >= rec_delay:
#                 detection = False
#                 timer_started = False
#                 out.release()
#                 print('Recording ended.')
#                 message_mail(sender_email, receiver_email, password, current_time, subject)
#         else:
#             timer_started = True
#             detection_stopped_time = time.time()

#     if detection:
#         out.write(frame)

#     for (x, y, width, height) in bodies:
#         cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)

#     for (x, y, width, height) in faces:
#         cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)

#     for (x, y, width, height) in eyes:
#         cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 4)

#     cv2.imshow("Camera", frame)

#     if cv2.waitKey(1) == ord('s'):
#         break

# out.release()
# cap.release()
# cv2.destroyAllWindows()