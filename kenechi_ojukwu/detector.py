import torch
import numpy as np
import torchvision
from PIL import Image
from deep_sort_realtime.deepsort_tracker import DeepSort
from utils.boundingbox_tools import scale_bbox, convert_to_xywh
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face

class DetectUniqueFaces:
    """This class detects and tracks faces from the given youtube video link
        
    Attributes
    ----------
    device : str
        string containing device type.E.g "cpu" or "cuda:0"

    mtcnn : MTCNN Object
        Contains the face detection module.

    deepsort_tracker : DeepSort Object
        Contains the deepsort module for object detection tracking.

    resnet : Resnet Object
        Contains the pre-trained Resnet model, used for face classification.

    
    Methods
    -------
    detect_face
        function used to detect the faces in a video frame.
    track_face
        function used to track faces in video frames.
    """

    def __init__(self):
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.mtcnn = MTCNN(factor=0.85, select_largest=False,keep_all=True, device=self.device)
        self.deepsort_tracker = DeepSort(max_age=15)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

    def detect_face(self, frame):
        """A function that detects the faces in a video frame. 
        
        Parameters
        ----------
        frame: PIL.array
            video frame
        Returns
        -------
        bboxs: list
            list of bounding box coordinates, scores, and class of detection.
        """
        # set resnet classifier
        self.resnet.classify = True
        bboxs = []
        scores = []
        # get bounding boxes and scores for each frame. bounding box format is (xmin,ymin,xmax,ymax)
        boxes, scores, _ = self.mtcnn.detect(frame, landmarks=True)

        if boxes is not None and scores is not None:
            for box, score in zip(boxes, scores):
                if box is not None and score is not None:
                    # create temporary frame so main frame is not altered 
                    temp_frame = frame.copy()
                    box = scale_bbox(*box)
                    # extract face from temporary frame
                    face = extract_face(temp_frame, box)
                    # get prediction to confirm if a face is in the bounding box.
                    logits =  self.resnet(face.unsqueeze(0))
                    probs = torch.sigmoid(logits)
                    probs.squeeze()
                    # if the prediction is greater than 25% then save the bounding box details
                    if probs[0][0] > 0.25:
                        result = (box, score, "face")
                        bboxs.append(result)

        return bboxs if len(bboxs) != 0 else None

    def track_face(self, frame, bboxs):
        """A function that tracks faces across video frames
        
        Parameters
        ----------
        frame: PIL.array
            This is the request data

        bboxs: list
            list of bounding box coordinates, scores, and class of detection.

        Returns
        -------
        tracked_unique_faces : list
            This is a list of cropped faces (arrays) and their IDs
        """
        tracked_unique_faces = []
        # deepsort tracker uses (x,y,w,h) bounding box coordinates
        bboxs = convert_to_xywh(bboxs)
        # convert PIL image to numpy image
        numpy_frame =  np.asarray(frame)
        tracks = self.deepsort_tracker.update_tracks(bboxs, frame=numpy_frame)

        # get all the ids and their faces
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            temp_frame = frame.copy()
            # scale bounding box by 30% to make cropping easier
            ltrb = scale_bbox(*ltrb, perc=30)
            ### get face for Id
            # get rid of negative values
            for i in range(len(ltrb)):
                if ltrb[i] <0:
                    ltrb[i] = -1 * ltrb[i]

            try:
                face = extract_face(temp_frame, ltrb)
            except:
                continue
            # save tracked id and face
            tracked_unique_faces.append((track_id, face))

        return tracked_unique_faces

    