import os
import settings
import functions as fns

# Create the directory to store the frames from the video with bounding boxes on the detected faces
if not os.path.exists(settings.FRAMES_PTH):
	os.makedirs(settings.FRAMES_PTH)

# Create to directory to store the extracted faces
if not os.path.exists(settings.FACES_PTH):
	os.makedirs(settings.FACES_PTH)


# 1. extract faces and generate embeddings for them. The embeddings are used for aggregating unique faces
embeddings_data = fns.extract_faces()

# 2. clustering the embeddings to get unique faces 
fns.cluster_imgs(embeddings_data)

# output
print()
print('Execution complete!')
print()
print('[INFO] Frames with bounding boxes on faces are stored in the path: {}'.format(settings.FRAMES_PTH)) 
print('[INFO] All extraced faces are stored in the path: {}'.format(settings.FACES_PTH)) 
print('[INFO] Montage of unique faces has been stored in the path: {}'.format(settings.UNIQUE_FACES_PTH)) 