------- Written by Daniel Ogunlolu --------

INFO:
Date: 30, NOV 2021
Programming Language: Python 3. 7
Main Script: extract-face.Python
Docker Base Image: orgoro/dlib-opencv-python

ALGORITHM:
1. Program starts by Downloading the given video from youtube link: 
https://www.youtube.com/watch?v=JriaiYZZhbY
2. Saves video inside directory (data/) with extension .mp4
3. Run HOG face detection on each frame, all detections are saved in data/faces directory
4. Finally, a Clustering process is performed on all faces to filter  unique faces
5. Unique faces are saved in data/unique_faces directory
6. When Program is done, enter q to end and exit the dockeer container

NOTE:
After building and running the docker image/container, you can copy directory containing 
faces extracted (data) using the following command:

docker cp <container id>:/main/data/ <host/path/to copy to/>

To view container id, use the following command:
docker ps

replace <host/path/to copy to/> with path where you want the data directory to be copied to.

eg: 
docker cp ad9f3d69bde2:/main/data/ /home/amazing/Desktop

RESULT:
Tested with the given video; the program did not work so well due to the fact that the given video has a bad quality and most 
of the faces appeared blurry (and very small). 

Tested the program with a diffrent video which has a better quality (faces were more vivid and clear) 
and the program worked well.

I have attached a zip files containing the final result (unique-faces)
