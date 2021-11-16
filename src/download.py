# Downloads the YouTube video and stores it in thedefined folder.
import logging
from pytube import YouTube

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', 
                    datefmt= '%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logger = logging.getLogger()
class YoutubeDownloader:

    def __init__(self, url, filepath):

        self.url = url
        self.filepath = filepath

    def download_url(self):

        yt = YouTube(self.url)
        video = yt.streams.get_highest_resolution()
        
        logger.info('Downloading...')
        video.download(self.filepath)
        logger.info('Download Complete')







