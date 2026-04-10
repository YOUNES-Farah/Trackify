import cv2
import face_recognition
import os  # Import os module to work with file paths
import time

# Initialize the camera
cap = cv2.VideoCapture(0)

# Define the "data" variable (if needed for your logic)
data = "CameraOuverte"

while True:
    if data == "CameraOuverte":
        print("ouverture de la camera")
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Load reference images from the "image" folder
        reference_encodings = []
        reference_names = []
        image_folder = "/home/pi/Desktop/reco/image"  # Path to your image folder
        for filename in os.listdir(image_folder):
            path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)[0]
            reference_encodings.append(encoding)
            reference_names.append(os.path.splitext(filename)[0])
        
        # Convert the frame from BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the RGB frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # For each detected face, try to recognize it
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(reference_encodings, face_encoding)
            distances = face_recognition.face_distance(reference_encodings, face_encoding)
            best_match_index = distances.argmin()

            # Draw a green box and the name of the recognized person if the match is good enough
            if matches[best_match_index] and distances[best_match_index] < 0.5:
                name = reference_names[best_match_index]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom), (right, bottom + 25), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f"{name} ({(1 - distances[best_match_index]) * 100:.2f}%)", (left + 2, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            # Draw a red box otherwise
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom), (right, bottom + 25), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, "Unknown", (left + 2, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Show the frame
        cv2.imshow("Face Recognition", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
