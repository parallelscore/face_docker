import os
import numpy as np
import logging
import pickle

import face_recognition
from src.face_extraction import ExtractFace


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', 
                    datefmt= '%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logger = logging.getLogger(__name__)


class FaceEncoding:
    
    def __init__(self):
        pass

    def encoding(self):
        
        logging.info('quantifying faces...')
        
        d_encoding = []
        face_extract = ExtractFace('C:/Users/USER/Desktop/Parallel_Score/video_data/')
        faces = face_extract.face_detect()
        
        for face in faces:

            
            boxes = face_recognition.face_locations(face, model='cnn')
            print(boxes)

            encodings = face_recognition.face_encodings(face, boxes)

            d_encoding.append(encodings)


        return d_encoding
            




