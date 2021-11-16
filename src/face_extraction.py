import os
import cv2
import logging
from PIL import Image
from numpy import asarray
import keras
from keras_preprocessing import image
from mtcnn.mtcnn import MTCNN


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', 
                    datefmt= '%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ExtractFace:

    def __init__(self, video_path):

        self.video_path = video_path
        

    def face_detect(self):
        
        logger.info('Reading Video using OpenCV')
        camera = cv2.VideoCapture(self.video_path)

        face_list = []
        while (len(face_list) <= 200):               #Running all images is computationally expensive using a CPU processor
            
            success, frame = camera.read()
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if success:
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                detector = MTCNN()
                faces = detector.detect_faces(frame)

                for i, face in enumerate(faces):
                    box = face['box']
                    if box != []:
                        
                        cropped_img = frame[box[1]: box[1] + box[3], box[0]: box[0] + box[2]]
                        #print(cropped_img)
            
                        face_list.append(cropped_img)
                        print(len(face_list))


            else:
                break

            
            cv2.waitKey(100)

        return face_list


                    





    
        