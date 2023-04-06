Unque Face Recognition Docker App

This is a test assessment for the AI Engineer role at Parallel Score

#### ALGORITHM:
- Step 1: Video request;
    - Download highest quality video from youtube using pytube
    - Save video in the `/app` directory
- Step 2: Facial Analysis;
    - Read in each frames in the video with opencv
    - Detect all faces in the frames and get their boundary boxes
    - For each faces detected get their facial embeddings (embeddings such as eyes landmark, nose landmark etc.)
    - Loop through each face boundary boxes gotten from the frame
    - While looping we calculate the distance between the current face embeddings to all previously unique face embeddings using L2 norm (np.linalg.norm) setting a tolerance of 0.6.
    - If the embeddings is unique, add it to the list of unique face embeddings and save the face. else; move on to the next embeddings
    
#### EXECUTION:
- Step 1: 
    - git clone https://github.com/parallelscore/face_docker.git
    - cd face_docker/Samuel_Taiwo

- Step 2:
    - Run `docker build -t unique-faces .`
    - After build, run; `docker run unique-faces`
    - Get container id with `docker ps -a`
    - Copy unique faces from docker; `docker cp <container_id>:/app/unique_faces/ ~/face_docker/Samuel_Taiwo`

#### Samuel Taiwo