from ultralytics import YOLO
import cv2
import cvzone
import math
import argparse
from sort import *
import utils

# Initilaize argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--youtube', type=str, required=True)
args = parser.parse_args()

# Initialize folder structure
folder_name = 'vids'  
image_folder = 'images'
result_folder = 'result'

folder_path = utils.path_finder(folder_name=folder_name, image_folder=image_folder, result_folder=result_folder)
cap = utils.youtube_downloader(youtube_link=args.youtube, folder_path=folder_path)

classNames = ['face']

# For Tracker
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# To assign output format of saved video
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
            if conf > 0.5:
                currentArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections, currentArray))

    resultTracker = tracker.update(detections)     

    for res in resultTracker:
        x1,y1,x2,y2,id = res
        x1,y1,x2,y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        w,h = x2-x1, y2-y1

        if x1 < 0: x1 = 0
        if y1 < 0: y1 = 0

        imgCrop = img[y1:y1+h, x1:x1+w]
        if face_list.count(id) == 0:
            face_list.append(id)
            cv2.imwrite('images/image' +str(id) + '.jpg', imgCrop)

        cvzone.putTextRect(img, f'ID: {int(id)}', (x1,y1), scale=1, thickness=1, colorR=(0,0,255))
        cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=1, colorR=(255,0,255))

    out.write(img)
    # cv2.imshow('Image', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
utils.remove_duplicates(image_folder=image_folder)