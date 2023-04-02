import cv2
import os

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

# To capture video from webcam.
# cap = cv2.VideoCapture(0)
# To use a video file as input
cap = cv2.VideoCapture('video_test.mp4')

if not os.path.exists('faces'):
    os.makedirs('faces')

currentFrame = 0
while True:
    # Read the frame
    ret, img = cap.read()

    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Save the face
        roi_color = img[y:y+h, x:x+w]
        file_name = f"face_{currentFrame}.jpg"
        cv2.imwrite(os.path.join('faces', file_name), roi_color)

    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

    currentFrame += 1

# Finished processing video
print("Finished processing video")

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
