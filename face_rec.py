import os
import time
import cv2
import numpy as np

# Capture and save faces from the camera feed.
def recognize_face_register(_):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    capture_interval = 1  # Set the capture interval to 1 second
    last_capture_time = time.time()
    i = 0  # Initialize i here

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.05, 5)

        current_time = time.time()

        if current_time - last_capture_time >= capture_interval:
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]  # Crop the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
                # Save the detected face as an image
                i += 1  # Increment i for each detected face
                face_filename = f"face_{i}.png"
                cv2.imwrite(face_filename, face)
                last_capture_time = current_time  # Update the last capture time

        cv2.imshow('frame', frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        
# Load known faces and names from the 'faces' directory.
def load_known_faces_and_names():
    known_faces = []
    known_names = []

    # Walk through the "faces" directory and its subdirectories
    for root, _, files in os.walk("faces"):
        for filename in files:
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(root, filename)
                known_image = cv2.imread(image_path)
                known_faces.append(known_image)

                # Extract the name from the relative path (assuming filename format is "name.jpg" or "name.png")
                relative_path = os.path.relpath(image_path, "faces")
                name = os.path.splitext(relative_path)[0].replace(os.path.sep, "_")  # Replace directory separators with underscores
                known_names.append(name.split("_")[0])

    return known_faces, known_names

# Recognize a face from the query face by comparing it with known faces.
def recognize_face(query_face, known_faces, known_names):
    if len(known_faces) == 0:
        return "No known faces"

    if len(query_face.shape) == 2:
        query_face = cv2.cvtColor(query_face, cv2.COLOR_GRAY2BGR)

    query_face_gray = cv2.cvtColor(query_face, cv2.COLOR_BGR2GRAY)

    min_msd = float('inf')
    matched_name = "Unknown"

    # Resize the query face to the dimensions of known faces
    query_face_gray = cv2.resize(query_face_gray, (known_faces[0].shape[1], known_faces[0].shape[0]))

    for i, known_face in enumerate(known_faces):
        known_face_gray = cv2.cvtColor(known_face, cv2.COLOR_BGR2GRAY)
        
        # Ensure query and known faces have the same dimensions for MSD calculation
        known_face_gray = cv2.resize(known_face_gray, (query_face_gray.shape[1], query_face_gray.shape[0]))

        msd = np.mean((query_face_gray - known_face_gray) ** 2)

        if msd < min_msd:
            min_msd = msd
            matched_name = known_names[i]

    return matched_name

# Perform face recognition for login using known faces and names.
def recognize_face_for_login():
    known_faces, known_names = load_known_faces_and_names()
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        best_match = None  # Store the best match found

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]

            # Compare the detected face with known faces
            matched_name = recognize_face(face, known_faces, known_names)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
            cv2.putText(frame, f"{matched_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if matched_name != "No known faces":
                best_match = matched_name

        cv2.imshow('Login', frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return best_match