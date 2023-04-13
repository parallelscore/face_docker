from ultralytics import YOLO
import cv2
import cvzone
import math
import argparse
from pytube import YouTube
from pytube.cli import on_progress
import os
import face_recognition
from sort import *

folder_name = 'vids'  
result_folder = 'result'
image_folder = 'images'

directory = os.getcwd() 

folder_path = os.path.join(directory, folder_name)

if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    print("Image folder created successfully")
else:
    print("Image folder already exist")

if not os.path.exists(result_folder):
    os.makedirs(result_folder)
    print("Result folder created successfully")
else:
    print("Result folder already exist")


if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("Video folder created successfully.")
else:
    print("Video folder already exists.")

parser = argparse.ArgumentParser()
parser.add_argument('--youtube', type=str, required=True)

# Parse the argument
args = parser.parse_args()

# Download Youtube Video
yt = YouTube(args.youtube,on_progress_callback=on_progress)
print('Downloading Youtube Video, please be patient...')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('./vids')

files = os.listdir(folder_path)

for file in files:
    file_path = os.path.join(folder_path, file)
    
    if file.endswith('.mp4') or file.endswith('.avi') or file.endswith('.mov'):
      cap  = cv2.VideoCapture(file_path)

# cap = cv2.VideoCapture('vids/BEST FOOTBALL HIGHLIGHTS BLACK TIGER 0 VS STAR WARRIORS 1 MALTI NAMKUM FOOTBALL TOURNAMENT 2021.mp4')
# FILE_PATH = "Videos/vid.mp4"


classNames = ['face']

# For Tracker
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# cap  = cv2.VideoCapture(FILE_PATH)

# TO assign output format of saved video
codec = cv2.VideoWriter_fourcc(*'XVID')
vid_fps =int(cap.get(cv2.CAP_PROP_FPS))
vid_width,vid_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('result/results.avi', codec, vid_fps, (vid_width, vid_height))

face_list = []

# Footballers Model
model = YOLO("yolo_weights/bestv2-80E.pt")

while True:
    _, img = cap.read()
    if not _:
        break

    results = model(img, stream=True)
    detections = np.empty((0,5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            w,h = x2-x1, y2-y1


            # Classname
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            # Confodence score
            conf = math.ceil(box.conf[0]*100)/100
            # if conf > 0.1:
            # cvzone.putTextRect(img, f'class: {currentClass}', (x1,y1), scale=1, thickness=1, colorR=(0,0,255))
            # cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=1, colorR=(255,0,255))
            currentArray = np.array([x1,y1,x2,y2,conf])
            detections = np.vstack((detections, currentArray))

    resultTracker = tracker.update(detections)     

    for res in resultTracker:
        x1,y1,x2,y2,id = res
        x1,y1,x2,y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        w,h = x2-x1, y2-y1

        # print("This is the lenght of the id", len(id))
        # for id in res:

        if x1 < 0: x1 = 0
        if y1 < 0: y1 = 0

        imgCrop = img[y1:y1+h, x1:x1+w]
        if face_list.count(id) == 0:
            face_list.append(id)
            cv2.imwrite('images/image' +str(id) + '.jpg', imgCrop)

        cvzone.putTextRect(img, f'ID: {int(id)}', (x1,y1), scale=1, thickness=1, colorR=(0,0,255))
        cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=1, colorR=(255,0,255))

    # out.write(img)
    cv2.imshow('Image', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Deleting duplicated images...")


# create a list of face encodings for all images in the folder
face_encodings = []
for filename in os.listdir(image_folder):
    image_path = os.path.join(image_folder, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if len(encoding) > 0:
        face_encodings.append(encoding[0])

# create a list of duplicate face encodings
duplicate_encodings = []
for i, encoding in enumerate(face_encodings):
    for j in range(i+1, len(face_encodings)):
        distance = face_recognition.face_distance([encoding], face_encodings[j])
        if distance < 0.6:  # threshold for similarity
            duplicate_encodings.append(j)

# remove duplicate images
for i in sorted(set(duplicate_encodings), reverse=True):
    filename = os.listdir(image_folder)[i]
    image_path = os.path.join(image_folder, filename)
    os.remove(image_path)


