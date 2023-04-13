import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import common
import cv2
import fastface as ff
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort
from deepface import DeepFace
from utils import downloadYouTubeVideo

#create directory to store the extracted faces

if not os.path.exists(common.FACES_PTH):
    os.mkdir(common.FACES_PTH)


# ============================================DOWNLOAD VIDEO====================================================== #

if os.path.exists(common.VIDEO_LOCATION):
    contents = os.listdir(common.VIDEO_LOCATION)
    if len(contents) == 0:
        print(" >>> Downloading Video from youtube link: {}".format(common.VIDEO_LINK))
        downloadYouTubeVideo(common.VIDEO_LINK)
        print(">>> Download Completed")
    else:
        pass
else:
    os.mkdir(common.VIDEO_LOCATION)
    print(" >>> Downloading Video from youtube link: {}".format(common.VIDEO_LINK))
    downloadYouTubeVideo(common.VIDEO_LINK)
    print(">>> Download Completed")

for file in os.listdir(common.VIDEO_LOCATION):
    if file.endswith('mp4'):
        video = file
        video_path = common.VIDEO_LOCATION + video
print(">>> Video name: {}".format(video))
print(">>> video path : {}".format(video_path))

"================================LOAD MODELS=================================="
model = ff.FaceDetector.from_pretrained('lffd_original').eval()
tracker = DeepSort(max_age=5)

"=================================== DETECT FACES============================="
def detectFace(frame):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    (preds,) = model.predict(frame,target_size = 640) #image needs to be resized to 640x640
    return preds


#convert prediction to required format
def convert(detections):
  bboxes = detections['boxes']
  scores = detections['scores']
  new_format = []
  for i in range(len(bboxes)):
    bbox = bboxes[i]
    x0,y0,x1,y1 = bbox
    new_format.append(([x0, y0, x1-x0, y1-y0],scores[i],0))
  return new_format


threshold_score = 3
def onVideo(video_path):
    video = cv2.VideoCapture(video_path)
    track_id_2_embedding = {} #to keep count of the unique tracking id and it's embeddings
    firstTime = True
    frameCount = 0

    while True:
        hasFrame,frame = video.read()
        if not hasFrame:
            break
        
        frameCount +=1
        detections = detectFace(frame)
        conv_detections = convert(detections)
        tracks = tracker.update_tracks(conv_detections,frame=frame)
        tracking_results = []

        for track in tracks:
            if not track.is_confirmed():
                continue
            tracking_results.append(np.append(track.to_ltrb().astype('int'),int(track.track_id)))
        if tracking_results:
            if firstTime:
                for i in range(len(tracking_results)):
                    x1,y1,x2,y2,track_id = tracking_results[i]
                    cropped_image = frame[y1:y2,x1:x2]
                    embedding = DeepFace.represent(cropped_image,enforce_detection=False,model_name='Facenet512')
                    #print(embedding_objs)
                    #embedding = embedding_objs[0]['embedding']
                    track_id_2_embedding[track_id] = embedding
                    face_folder_path = f'{common.FACES_PTH}faces-{track_id}/'
                    if not os.path.exists(face_folder_path):
                        os.makedirs(face_folder_path)
                    face_path = f'{face_folder_path}frame{frameCount}-{i}.jpg'
                    cv2.imwrite(face_path,cv2.resize(cropped_image,(100,100)))
                    if i+1 == len(tracking_results):
                        firstTime = False       
            else:
                for i in range(len(tracking_results)):
                    x1,y1,x2,y2,track_id = tracking_results[i]
                    cropped_image = frame[y1:y2,x1:x2]
                    face_path = f'{common.FACES_PTH}faces-{track_id}/frame{frameCount}-{i}.jpg'
                    if track_id not in track_id_2_embedding:
                        try:
                            target_embedding = DeepFace.represent(cropped_image,enforce_detection=False,model_name='Facenet512')
                        except cv2.error:
                            continue
                        #target_embedding = embedding_objs[0]['embedding']
                        distances = []
                        for emb in list(track_id_2_embedding.values()):
                            distance = np.linalg.norm(np.array(target_embedding) -np.array(emb))
                            distances.append(distance)
                        if min(distances) <= threshold_score:
                            closest_track_id = list(track_id_2_embedding.keys())[np.argmin(distances)]
                            face_path = f"{common.FACES_PTH}faces-{closest_track_id}/frame-{frameCount}-{i}.jpg"
                            cv2.imwrite(face_path,cv2.resize(cropped_image,(100,100)))
                        else:
                            face_folder_path = f'{common.FACES_PTH}faces-{track_id}/'
                            if not os.path.exists(face_folder_path):
                                os.makedirs(face_folder_path)
                            face_path = f'{face_folder_path}frame{frameCount}-{i}.jpg'
                            track_id_2_embedding[track_id] = target_embedding
                            cv2.imwrite(face_path,cv2.resize(cropped_image,(100,100)))
                    else:
                        try:
                            cv2.imwrite(face_path,cv2.resize(cropped_image,(100,100)))
                        except cv2.error:
                            continue
                        
        print(f"frameCount{frameCount}")


def main():
    onVideo(video_path)
    print(">>> Done")
    print(f">>> unique faces saved to {common.FACES_PTH} directory")



if __name__ == "__main__":
    main()






