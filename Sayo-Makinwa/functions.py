import face_recognition
import cv2
import pafy #requires youtube_dl
from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np

import settings


def get_embeddings(frame, faces, frame_count):
    # I used the 'face_recognition' library to train the embeddings
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # face_recognition requires images to be in RGB format as opposed to opencv's BGR
    embeddings = face_recognition.face_encodings(rgb_frame, faces)

    d = [
        {
            'path': '{}/frame{}_face{}.jpg'.format(settings.FACES_PTH, frame_count, i),
            'loc': face, 'embedding': embed
        } 
        for i, (face, embed) in enumerate(zip(faces, embeddings))
    ]

    return d


def extract_faces():
    # stream the youtube video and generate a path usable by opencv VideoCapture
    video = pafy.new(settings.STREAM_PTH)
    best = video.getbest(preftype='mp4')
    cap = cv2.VideoCapture(best.url)

    # load opencv's cascade classifier 
    face_cascade = cv2.CascadeClassifier(settings.CASCADE_PTH)

    frame_count = 0 # counter for keeping track of the number of faces

    embeddings_data = [] # list to store data of the embeddings to save for later use
    while(True):
        ret, frame = cap.read()

        if ret: # if this frame was successfully captured
            # EXTRACTION OF FACES
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale, required by opencv's cascade classifier
            faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect the faces
            
            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # Draw a green bounding box around each face on the frame
                face = frame[y:y+h, x:x+w]
                cv2.imwrite('{}/frame{}_face{}.jpg'.format(settings.FACES_PTH, frame_count, i), face) # store each face in a folder

            cv2.imwrite('{}/{}.jpg'.format(settings.FRAMES_PTH, frame_count), frame) # store frame after all bounding boxes have been drawn on it
            cv2.imshow('Video frames', frame) # visualization of the frames

            
            # TRAINING EMBEDDINGS FOR THE FACES FOR APPROXIMATING UNIQUE FACES
            d = get_embeddings(frame, faces, frame_count)
            embeddings_data.extend(d)

        # Press q to close the video windows before it ends if you want
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        
        frame_count += 1
        if settings.MAX_FRAMES is not None and frame_count >= settings.MAX_FRAMES: # run until MAX_FRAMES
            break

    print('[INFO] Total number of frames analyzed: {}'.format(frame_count))
    print('[INFO] Total number of potential faces extracted: {}'.format(len(embeddings_data)))

    # with open(settings.EMBEDDINGS_PTH, "wb") as f:
    #     print('[INFO] Saving the embeddings of faces to file in the path: {}'.format(settings.EMBEDDINGS_PTH))
    #     f.write(pickle.dumps(embeddings_data))

    cap.release()
    cv2.destroyAllWindows()

    return embeddings_data


def cluster_imgs(embeddings_data):
    embeddings = [data['embedding'] for data in embeddings_data]

    clt = DBSCAN(metric='euclidean')
    clt.fit(embeddings)

    unique_ids = np.unique(clt.labels_)
    no_unique_faces = len(np.where(unique_ids > -1)[0]) # exclude outliers 
    print('[INFO] Number of unique faces found after clustering: {}'.format(no_unique_faces)) 

    faces = []
    for unique_id in unique_ids: 
        idxs = np.where(clt.labels_ == unique_id)[0] 
        # idxs = np.random.choice(idxs, size=1, replace=False) 
        idxs = idxs[0]

        face = cv2.imread(embeddings_data[idxs]['path'])
        
        face = cv2.resize(face, (100, 100)) # resize the face and add it to the faces montage list 
        faces.append(face)

    montage = build_montages(faces, (100, 100), (
        np.ceil(np.sqrt(len(faces))), 
        np.floor(np.sqrt(len(faces)))
    ))[0]

    cv2.imwrite(settings.UNIQUE_FACES_PTH, montage)

    cv2.imshow('Unique faces', montage)
    cv2.waitKey(20)

    cv2.destroyAllWindows()

