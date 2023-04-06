# Face Detector

Solution Repository for the Task of detecting faces in the provided video link.

### Repository Breakdown:

 1. ```main.py```: This script contains the main function used to run the application.
 2. ```detector.py```: This script contains the class used to detect and track the faces in the video.
 3. ```video_handler.py```: This script contains the class used to handle video download and frames extraction.
 4. ```utils/boundingbox_tools.py```: This is a utility script for handling bounding boxes.
 5. ```utils/video_frame_skipper.py```: This is a utility script used to skip video frames, if needed.
 6. ```Dockerfile```: Docker file for face detection application.

### How to run application:

1. Build the docker image, using the command below:

    ```docker build -t face-detector .```
    
2. After successful build: run the application with:

   using your git terminal on a windows system:

   ```docker run --rm -v /$PWD/unique_faces_folder:/app/src/unique_faces_folder face-detector --cli_display=True```

   using linux based systems:

   ```docker run --rm -v $PWD/unique_faces_folder:/app/src/unique_faces_folder face-detector --cli_display=True```
   
 ### Command Line Tag Breakdown:

1. ```--skip```: If set to True, some video frames will be skipped in order to reduce the length of the overall video. Default: False.
2. ```--video_link```: String containing the youtube video link, pass in youtube video url. Default: "https://www.youtube.com/watch?v=JriaiYZZhbY&t=4s"
3. ```--output_path```: String containing the folder path to save faces extracted from video. Default: "unique_faces_folder/"
4. ```--n_steps```: An int value, indicates the number of steps to take in order to get indexes of key frames in the video. Default: 100.
5. ```--n_frames```: An int value, indicates the number of frames indexes to get inbetween key frames indexes. Default: 50. 
6. ```--cli_display```: bool value, if True, it displays the progress of the application as it runs. Default: False


### Note:
The provided video is 17 minutes 42 seconds long, in terms of video frames, it contains 26,555 frames. Were there are 25 frames per second.
If using the skip functionality with default settings, the stated number of frames is reduced to 13,250 frames, resulting to approximately 8 mintues worth of content.
The idea of video frame skipping is to reduce the overrall face extraction time when running on cpu.

After 10 seconds worth of video content (1500 frames) have been processed, here is a link to the sample of faces extracted:[link](https://drive.google.com/drive/folders/1Ch_0POxseYeXZEUMrnXm4N7BXDFrOQ4H?usp=share_link).

The faces appear to be blurry due to the high motion of both the players and the camera man.
