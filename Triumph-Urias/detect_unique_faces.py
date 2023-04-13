# -*- coding: utf-8 -*-
"""detect_unique_faces.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ibra9Tsv52nOAcCdhPuOaC_RCakOW8Zm
"""

# pip install -q opencv-python numpy dlib imutils pytube

import os 
import shutil
import cv2
import numpy as np
import dlib
import imutils

from imutils import face_utils
from pytube import YouTube

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input

from sklearn.cluster import KMeans


#### Helper Functions

# Download Video
def download_video(link, path):
  print(" >>> Downloading Video.......")
  yt = YouTube(link)
  yt_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
  yt_stream.download(path)
  print(" >>> Video Download Successful !")

# Detect Faces
def detect_faces(frame, frame_no):
  print(f"\n >>> Checking for Faces in Frame {frame_no}")
  # Convert frame to grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Detect faces in grayscale frame image
  rects = detector(gray, 0)

  # Loop over faces
  for rect in rects:
    print(" >>> Handling Boxes.......")
    # Extract facial landmarks
    shape = predictor(gray, rect)
    # face_descriptor = np.array([shape.part(i).x for i in range(68)] + [shape.part(i).y for i in range(68)])

    (x, y, w, h) = face_utils.rect_to_bb(rect)
    face = frame[y:y+h, x:x+w]

    if face.size == 0:
      continue
    
    # Resize and add face image to list of faces
    face = cv2.resize(face, (224, 224))
    faces.append(face)
  
  print(f" >>> All {frame_no} Frame(s) Checked Successfully !")

# Test Uniqueness
def test_uniqueness(faces):
  print("\n >>> Testing Uniqueness of Faces......")
  model = VGG16(weights="imagenet", include_top=False)
  for i, face in enumerate(faces):
    print(f" >>> Progress: {i} / {len(faces)}", end="\r")
    img_data = np.asarray(face)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    features_list.append(features.flatten())
  
  print("\n >>> Clustering Faces......")
  clusters = KMeans(random_state=42).fit(np.array(features_list))

  print("\n >>> Saving Unique Faces.......")
  used_labels = []
  for i, label in enumerate(clusters.labels_):
    if label not in used_labels:
      used_labels.append(label)
      file_path = IMAGES_DIR + "Face_" + str(label)
      cv2.imwrite(file_path, faces[i])
  print("\n >>> Images Saved Successfully !")


if __name__ == "__main__":
 
  IMAGES_DIR = "/images"

  VIDEO_LINK = "https://www.youtube.com/watch?v=JriaiYZZhbY&t=4s"

  # VIDEO_LINK = "https://www.youtube.com/watch?v=Xygk7UjKM2g"

  if os.path.exists(IMAGES_DIR):
    shutil.rmtree(IMAGES_DIR)

  os.makedirs(IMAGES_DIR)

  print("[INFO:] Container Started \n \n")
  download_video(link=VIDEO_LINK, path=".")

  for file in os.listdir():
    if file.endswith("mp4"):
      video = file
  print(f" >>> Video name: {video} \n")

  # Load face detector and facial landmark estimator
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

  # Open the video file
  cap = cv2.VideoCapture(video)

  # Initialize variables
  frame_no = 0
  faces = []
  features_list = []

  print(" >>> Video Processing Started.........")

  # if cap.isOpened():
  # Loop over frames
  while True:
    # Read frames from downloaded video
    ret, frame = cap.read()

    frame_no += 1
    
    # Stop when reading is unsuccessful due to bad file or video has ended
    if not ret:
      print(" >>> Reached the end of video or can't receive frame \n \n")
      break

    # Resize frame to speed up processing
    frame = imutils.resize(frame, width=500)

    # Detect face
    detect_faces(frame, frame_no)

  # Release video
  cap.release()

  # Test face uniqueness
  test_uniqueness(faces)

print("[INFO:] Exiting Container......")

