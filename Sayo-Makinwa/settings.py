# paths

CASCADE_PTH = 'haarcascade_frontalface_default.xml' # path to file that contains info about structure of faces for opencv's cascade classifier to detect faces
FRAMES_PTH = 'frames' # directory to store frames from video with bounding boxes on faces
FACES_PTH = 'extracted_faces' #  to store the extracted faces
STREAM_PTH = 'https://www.youtube.com/watch?v=JriaiYZZhbY'

EMBEDDINGS_PTH = 'embeddings.pkl' # path to store the embeddings of the faces. Used to find unique faces
UNIQUE_FACES_PTH = 'unique_faces.jpg' # path to store a collage of unique faces

"""
Set this to None to use all the frames in the video. 
Otherwise, assign a number for the maximum number of frames to use (perhaps for testing purposes)
"""
MAX_FRAMES = 100 #None 
