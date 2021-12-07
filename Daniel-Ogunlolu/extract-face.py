import os
os.chdir("data") 
imdir = 'faces'
targetdir = "unique-faces"
video_link = 'https://youtu.be/JriaiYZZhbY' #link to youtube video 
number_clusters = 7 #number of cluster for unique face
frame_skip = 5 #skip every fifth frame (makes the detection process faster)

if not os.path.isdir(imdir):
        os.mkdir("faces")
if not os.path.isdir(targetdir):
        os.mkdir(targetdir)

# -----------------------------------DOWNLOAD VIDEO------------------------------------------------- #
from pytube import YouTube

# function to download youtube video
def downloadYouTube(videourl, path):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)

print("\n \nContainer Started")
print(" >>> Downloading Video from youtube link: {}".format(video_link))
downloadYouTube( video_link,'.')
print(" >>> Download done ")

for file in os.listdir():
    if file.endswith("mp4"):
        video = file

print(" >>> Video name: {}".format(video))


# -----------------------------------FACE DETECTION------------------------------------------------- #

import cv2
import dlib
from imutils import face_utils


face_detect = dlib.get_frontal_face_detector()
#uncomment this to use cnn face detection whiich is slower
#face_detect = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")
frame_no = 0
video_capture = cv2.VideoCapture(video)


#face detection fuction
def detect_face(frame):
    frame_original = frame
    global frame_no

    if frame_no%frame_skip == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detect
        rects = face_detect(gray, 1)

        detect = 1
        for (i, rect) in enumerate(rects):
            detect = 2
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # save face
            cv2.imwrite("faces/frame-{}-face-{}.jpg".format(str(frame_no), str(i)),cv2.resize(frame_original[y:y+h, x:x+w], (200,200)))


    #return frame with detection
    return frame, detect

print(" >>> Using HOG to detect Faces in all frames (this will take a while)..........")

while True:
    # Capture frame
    ret, frame = video_capture.read()
    

    if ret == 0:
        break

    # Display the frame with detection
    try:
        show, detect= detect_face(frame)
        #cv2.imshow('Video', show)
    except Exception as e:
        #print(" >>> can not display video due to this error: {}".format(e))
        pass
    frame_no = frame_no + 1

    # Quit video by typing Q
    if cv2.waitKey(detect) & 0xFF == ord('q'):
        break

print(" >>> Reach end of Video or Can't receive frame")
print(" >>> Done, existing video window  and saving detected face")

video_capture.release()
#cv2.destroyAllWindows()

print(" >>> Detected faces saved to faces Directory. \n ------------------------------------------------------------------------------------------------\n")

# -----------------------------------FACE CLUSTTERING------------------------------------------------- #
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.cluster import KMeans
import os.path
image.LOAD_TRUNCATED_IMAGES = True 
model = VGG16(weights='imagenet', include_top=False)

# Variable
images = []

print("\n \n -------------------------------------------------------------------------------------------------------------------------------------------")
print(" >>> Performing Face Clustering to detect unique faces in faces saved in faces directory")
# Loop over files and get features
filelist = os.listdir(imdir)
for i, m in enumerate(filelist):
    filelist[i]= imdir + "/" + m
    images.append(cv2.imread(filelist[i]))
featurelist = []
for i, imagepath in enumerate(filelist):
    print(" >>> Status: %s / %s" %(i, len(filelist)), end="\r")
    img = image.load_img(imagepath, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    featurelist.append(features.flatten())

# Clustering
kmeans = KMeans(n_clusters=number_clusters, random_state=0).fit(np.array(featurelist))

print("\n")

for i, label in enumerate(kmeans.labels_):
    dir = targetdir  +  "/" +"face-"+ str(label)
    name = targetdir + "/"  +"face-"+ str(label) + "/" + str(i) + ".bmp"
    try:
        if not os.path.isdir(dir):
            os.mkdir(dir)
        cv2.imwrite(name, images[i])
    except Exception as e:
        pass
    

print(" >>> Done")
print(" >>> Unique Faces saved to Unique-face directory")
print(" >>> Press q to exit program")

while (input(" >>> ") != 'q'):
    pass

print("Exiting......")