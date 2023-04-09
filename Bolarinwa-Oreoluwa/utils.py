from pytube import YouTube
from pytube.cli import on_progress
def downloadYouTubeVideo(video_link):
    yt = YouTube(video_link,on_progress_callback=on_progress)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('./video')

    