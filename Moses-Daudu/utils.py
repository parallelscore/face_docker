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
