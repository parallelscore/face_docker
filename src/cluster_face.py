
from sklearn.cluster import DBSCAN
from src.encode_face import FaceEncoding
import numpy as np
import pickle
import logging


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', 
                    datefmt= '%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


logger = logging.getLogger(__name__)



class Clustering:

    def __init__(self, jobs=-1):

        self.jobs = jobs
        
    def cluster_embedding(self):

        logger.info("Loading encondings...")
        # data = np.array(data)
        encodings = FaceEncoding().encoding() 
        print(encodings)
        logger.info('clustering...')
        
        clt = DBSCAN(metric="euclidean", n_jobs=self.jobs)
        clt.fit(encodings)

        labelIDs = np.unique(clt.labels_)

        numUniqueFaces = len(np.where(labelIDs > -1)[0])
        logger.info(" Number of unique faces: %s", numUniqueFaces)

        return numUniqueFaces

