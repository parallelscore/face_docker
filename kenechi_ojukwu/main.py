import os
import torch
from PIL import Image
from fire import Fire
import torchvision.transforms as T
from detector import DetectUniqueFaces
from video_handler import VideoHandler

def printt(output):
    print(output, flush=True)

def get_faces(skip=False, video_link = "https://www.youtube.com/watch?v=JriaiYZZhbY&t=4s", output_path="unique_faces_folder/", n_steps=100, frame_count=50, cli_display=False):
    """This function gets the faces in the url link. 
        
        Parameters
        ----------
        skip: bool
            if true, reduce the number of video frames to reduce the overall face extraction time. Default: False

        video_link: str
            string containing the video url.

        output_path: str
            string containing path to store extracted faces.

        n_steps : int
            number of steps to take to get key frames. 100 steps is ideal, The lower the better. The higher, the more discontinuity in video frames.

        n_frames: int
            number of frames to get inbetween key frames.

        cli_display: str
            display text on the cli. Helps keep track of progress.

        Returns
        -------
    """
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    uniq_faces = set()
    unique_face_tracker = DetectUniqueFaces()
    TensorPilTransformer = T.ToPILImage()

    face_count = 0
    video_frame_count = 0
    
    if skip:
        video_handler = VideoHandler(skip=skip,n_steps=n_steps, frame_count=frame_count)
    else:
        video_handler = VideoHandler()
    
    
    
    if not os.path.isfile(video_handler.video_path):

        if cli_display:
            printt("Downloading Video ...")
        # download and rename video file
        video_handler.download_video(video_link)
        video_handler.rename_video_file()
        if cli_display:
            printt("Download is successful.")
            printt("Getting Frames ...")

    # get video frames
    video_frames = video_handler.get_video_frames()

    if cli_display:
        printt("Extracting Faces From Frames ...")

    for frame in video_frames:
        # convert numpy array to PIL.array 
        frame = Image.fromarray(frame)

        # get bounding box of faces in a frame
        bbox = unique_face_tracker.detect_face(frame)
        if bbox:
            # track and save the predicted faces
            tracked_faces = unique_face_tracker.track_face(frame, bbox)
            if len(tracked_faces) != 0:
                for info in tracked_faces:
                    if info[0] not in uniq_faces:
                        uniq_faces.add(info[0])
                        face = info[1]
                        face = face*255
                        face = TensorPilTransformer(face)
                        face.save(f'{output_path}{info[0]}.jpg')
                        face_count += 1
                        if cli_display:
                            printt(f"Faces Saved: {face_count}")

        video_frame_count += 1
        if cli_display:
            printt(f"Frame Count: {video_frame_count}")
            if video_frame_count%25 == 0:
                printt(f"{video_frame_count/25} second(s) worth of the video has been analyzed.")

            if (frame_count/25) / 60  == 0:
                printt(f"{ (video_frame_count/25) / 60} minute(s) worth of the video has been analyzed.")
    if cli_display:          
        printt("Done!")                
        printt(f"Number of Tracked Faces: {face_count}")


if __name__ == '__main__':
    Fire(get_faces)