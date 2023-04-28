# Capture Unique Faces In A Blury Video

Hi my name is `Moses Daudu` 

# The difference with new version
1. The Pytube API is not working as at the moment of making this pull request, however there is a condition that runs the code even when the youtube aargument is not specified. Please read the `Run with docker` for more info.
2. The `face_recognition` package has been removed. The library does not capture the face embedding well, and so it does not perform adequately and as expected. The sort algorithm already does a great job of identifying the unique faces. I tested the effectiveness of both sort and deepsort, using the mobilenet embedding for deepsort. Sort performed better than deepsort, however, there are other tracking algorithms that will perform better, but the trade of is that it will require more computations and result in a slower runtime especially without GPU.
3. The major thinsg to note is to run the docker file without including the youtube argument, however, once the pytube API is back online, the youtube argument can be used as indicated in the `Run with docker` section.
4. The `football_video` file is the first 45 seconds of the football match. Due to GitHub limitations, the whole video could not be uploaded.

# How the code works
Firstly you would need to input the youtube link to the football video you want to analyze.
The algorithm then creates three seperate folders which are images, result and vids.
The images folder is where all the face images will be saved, the result folder is where the output video will be saved, and the vids folder is where the youtube linked video will be dowloaded and saved.
The algorithm takes the saved video and runs it through a custom model that was trained on over 5000 face images. It then saves the images in the images folder and then lastly the face_recognition package is used to encode the images in the folder to identify images that are similar and then deletes the similar face images. 

It is important to mention that within the code, the sort algorithm already ensures that the same face is not given multiple IDs by increasing the max_age argument. This means that only unique IDs are captured, and in cases where the same face is given another ID, the face_recognition package ensures that those images are deleted.

The code is reusable, meaning that you could use it for a particular youtube link and then use it with another youtube link. It ensures to run the latest video downloaded.

## Run without Docker:

Create virtual environment and install requirements like below:

`pip install -r requirements.txt`

Run Python file
`python face_detect.py`

## When the Pytube API returns, RUN
`python face_detect.py --youtube="https://youtu.be/JriaiYZZhbY"`
please note that you can change the youtube link to whatever link you may choose

Check the `result` folder for the video recording and check the `images` folder for the Unique face images



## Run with Docker:
Build the dockerfile
`docker build -t face_detect .`

Run the dockerfile
`docker run face_detect`

## When the Pytube API returns, RUN
`docker run face_detect --youtube="https://youtu.be/JriaiYZZhbY"`

Check the `result` folder for the video recording and check the `images` folder for the Unique face images

![Header](screen01.png)
![Header](screen02.png)
