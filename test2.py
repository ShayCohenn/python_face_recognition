import numpy as np
import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)

    for i, (x, y, w, h) in enumerate(faces):
        face = frame[y:y+h, x:x+w]  # Crop the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
        
        # Save the detected face as an image
        face_filename = f"face_{i}.png"
        cv2.imwrite(face_filename, face)

    cv2.imshow('pook', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
