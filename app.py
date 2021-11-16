import os
from src.download import YoutubeDownloader
from src.face_extraction import ExtractFace

# from src.encode_face import FaceEncoding
from src.cluster_face import Clustering

# Downloading youtube video via the link

if __name__ == '__main__':
    os.mkdir('video')
    youtube_video = YoutubeDownloader("https://www.youtube.com/watch?v=mnAnZmryS5o", "video/")
    youtube_video.download_url()

    cluster = Clustering()
    labels = cluster.cluster_embedding()

    print(f'The number of unique faces {labels}')


