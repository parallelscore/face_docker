import os
import sys
from pytube import YouTube
from pytube.exceptions import LiveStreamError, RegexMatchError

ROOT_DIR = os.getcwd()
sys.path.insert(0, ROOT_DIR)

def download_yt_video(yt_url: str) -> os.PathLike:
    video_path = os.path.join(ROOT_DIR, "app")
    rname_vid = 'video.mp4'
    try:
        yt = YouTube(yt_url)
        print ("------- Downloading Youtube Video -------")
        ys = yt.streams.get_highest_resolution()
        ys.download(f'{video_path}')
        new_fname = f'{video_path}/{ys.default_filename}'
        os.rename(new_fname, rname_vid)
    except Exception as reason:
        print (f"Exception occured: {reason}")
                        

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=JriaiYZZhbY&t=4s"
    download_yt_video(url)