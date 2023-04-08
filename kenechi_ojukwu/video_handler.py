import os
import cv2
from pytube import YouTube
from utils.video_frame_skipper import SkipFrames


class VideoHandler:
    """This class handles downloading the video and extracting frames the video.
        
    Attributes
    ----------
    skip : str
         if true, reduce the number of video frames to reduce the overall face extraction time. Default: False

    local_path : str
        String containing the path to save video.

    frame_skipper : frameSkipper Object
        Object used to skip frames, if needed.

    video_path : str
        path to video file.


    Methods
    -------
    download_video:
        function downloads the video from youtube.
    rename_video_file
        function used rename the video file.
    get_video_frames
        function used to extract the frames from the video.
    """

    def __init__(self, skip=False, n_steps=100, frame_count=50):
        self.skip = skip
        self.local_path = "local_video_path/"
        self.frame_skipper = SkipFrames(n_steps=n_steps, frame_count=frame_count)
        if not os.path.isdir(self.local_path):
            os.mkdir(self.local_path)
    
        self.video_path = self.local_path + "video.mp4"



    def download_video(self, video_link):
        """A function that downloads the video from youtube.
        
        Parameters
        ----------
        video_link: str
            video url
        Returns
        -------
        """
        video_object = YouTube(video_link)
        video_object = video_object.streams.get_highest_resolution()
        try:
            video_object.download(self.local_path)
        except:
            raise Exception("An error has occurred during download!")

    def rename_video_file(self):
        """function used rename the video file."""
        filename =  os.listdir(self.local_path)
        new_name = "video.mp4"

        if filename[0] == "":
            raise Exception("Video does not exist in directory, check to see if it downloaded properly.")

        old_file = self.local_path + filename[0]
        new_file = self.local_path + new_name

        os.rename(old_file,new_file)

    def get_video_frames(self):
        """Function that gets the frames from the video file.
        
        Parameters
        ----------
        
        Returns
        -------
            frame: generator
                generator object of the extracted frames.
        """

        if not os.path.isfile(self.video_path):
            raise Exception("Video has probably not being renamed.")

        video = cv2.VideoCapture(self.video_path)
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_idx = 0
        idx = 0
        if self.skip:
            indexes = self.frame_skipper.extract_n_frames(length)

        while video.isOpened():
            success, frame = video.read()
            if success:
                if self.skip:
                    if idx >= len(indexes):
                        break
                    if indexes[idx] == frame_idx:
                    
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        idx +=1
                        yield frame
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    yield frame

            else:
                break
            frame_idx += 1


