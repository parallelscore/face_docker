from pytube import YouTube
from pytube.cli import on_progress
import os
import face_recognition
import cv2

def path_finder(folder_name, image_folder, result_folder):

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

    return folder_path

def youtube_downloader(youtube_link, folder_path):
    # Download Youtube Video
    yt = YouTube(youtube_link,on_progress_callback=on_progress)
    print('Downloading Youtube Video, please be patient...')
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(folder_path)

    files = os.listdir(folder_path)
    file_path = os.path.join(folder_path, files[-1])
    
    if files[-1].endswith('.mp4') or files[-1].endswith('.avi') or files[-1].endswith('.mov'):
        cap  = cv2.VideoCapture(file_path)
        return cap
        
def remove_duplicates(image_folder):
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

    print("Successfully Deleted duplicated images!!!")
    