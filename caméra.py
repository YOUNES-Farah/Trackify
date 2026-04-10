import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)  # Ensure the correct camera index
while True:
    ret, frame = camera.read()
    if not ret:
        break
    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
