from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *
import argparse
import utils

class ObjectDetection():

    def __init__(self):
        self.model = self.load_model()
        self.CLASS_NAMES_DICT = self.model.model.names

    def load_model(self):
        model = YOLO('./yolo_weights/bestv2-80E.pt')
        model.fuse()

        return model
    
    def predict(self, img):
        results = self.model(img, stream=True)
        return results
    
    def plot_boxes(self, results, img, detections):

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1,y1,x2,y2 = box.xyxy[0]
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                w,h = x2-x1, y2-y1

                # Classname
                cls = int(box.cls[0])
                currentClass = self.CLASS_NAMES_DICT[cls]

                # Confodence score
                conf = math.ceil(box.conf[0]*100)/100

                if conf > 0.5:
                    currentArray = np.array([x1,y1,x2,y2,conf])
                    detections = np.vstack((detections, currentArray))
                    
        return detections, img
   
    def track_detect(self, detections, img, tracker):
        face_list = []
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

            cvzone.putTextRect(img, f'ID: {id}', (x1,y1), scale=1, thickness=1, colorR=(0,0,255))
            cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=1, colorR=(255,0,255))

        return img

    def __call__(self):

        # Initilaize argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument('--youtube', type=str)
        args = parser.parse_args()

        # Initialize folder structure
        folder_name = 'vids'  
        image_folder = 'images'
        result_folder = 'result'

        folder_path = utils.path_finder(folder_name=folder_name, image_folder=image_folder, result_folder=result_folder)
        
        if args.youtube:
            cap = utils.youtube_downloader(youtube_link=args.youtube, folder_path=folder_path)
        else:
            cap = cv2.VideoCapture('football_video.mp4')
        assert cap.isOpened()

        codec = cv2.VideoWriter_fourcc(*'XVID')
        vid_fps =int(cap.get(cv2.CAP_PROP_FPS))
        vid_width,vid_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter('result/results.avi', codec, vid_fps, (vid_width, vid_height))

        tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

        while True:

            _, img = cap.read()
            assert _
            
            detections = np.empty((0,5))
            results = self.predict(img)
            detections, frames = self.plot_boxes(results, img, detections)
            detect_frame = self.track_detect(detections, frames, tracker)
            out.write(detect_frame)
        
        
    
detector = ObjectDetection()
detector()
