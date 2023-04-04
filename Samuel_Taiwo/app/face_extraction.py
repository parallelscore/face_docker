
import os
import sys
import cv2
import numpy as np
import torch
from PIL import Image
import face_recognition
#from facenet_pytorch import MTCNN, InceptionResnetV1

# Load FaceNet model
#facenet_model = InceptionResnetV1(pretrained='vggface2').eval()

ROOT_DIR = os.getcwd()
sys.path.insert(0, ROOT_DIR)

output_folder = os.path.join(ROOT_DIR, "unique_faces")
video_path = os.path.join(ROOT_DIR, "video.mp4")

if not os.path.exists(output_folder):
    os.mkdir("unique_faces")

# Load the video

cap = cv2.VideoCapture(video_path)

# Initialize MTCNN
#mtcnn = MTCNN(margin=30, keep_all=True, post_process=False)#, device='cuda:0')

unique_faces = {}  # list to store unique faces

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    boxes = face_recognition.face_locations(frame)

    if boxes is None:
        continue
        
    encodings = face_recognition.face_encodings(frame, boxes)#[0]

    for i, box in enumerate(boxes):
    #for encoding in encodings:

        is_unique = True

        for filename, existing_encoding in unique_faces.items():
            
            # using np.linlang.norm in background
            matches = face_recognition.compare_faces([encodings[i]], existing_encoding, tolerance=0.6)
            # matches return true if they are similar
            print (matches)
            
            if matches[0] == True:
                is_unique = False
                break

        if is_unique:

            # add 20 pixels to each side of the detected face
            top, right, bottom, left = box
            #face_height = bottom - top
            #face_width = right - left
            top = max(0, top - 20)
            bottom =  min(frame.shape[0], bottom + 20)
            left = max(0, left - 20)
            right = min(frame.shape[1], right + 20)
            
            face = frame[top:bottom, left:right] 
            filename = os.path.join(output_folder, f'face_{len(unique_faces)}.jpg')
            face_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
            face_image.save(filename)
            unique_faces[filename] = encodings[i]

cap.release()

