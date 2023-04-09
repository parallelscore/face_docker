# ------- Written by Bolarinwa Oreoluwa --------

## INFO:

Date: 09, APRIL 2023

Programming Language: Python 3

Main Script: main.py

Docker Base Image: orgoro/dlib-opencv-python

### ALGORITHM:
1. Program starts by Downloading the given video from youtube link: 
https://www.youtube.com/watch?v=JriaiYZZhbY
2. Saves video inside directory (video/) with extension .mp4
3. Run Face Detection, then perform tracking
4. If the track ID is still the same, crop the image and push it to the required folder.
5. If the event has a new ID:

    a. Take a similarity measure of the image.
    
    b. If the similarity measure is close to something we've seen before:
    
    c. Push the image to the required folder.
    
    d. If the similarity measure is not close to anything we've seen before:
    
        i. Create a new folder.
        ii. Capture the embeddings of the new image.
        
6. Repeat steps 3,4,5

## RESULT:

Tested with the given video; the program did not work so well due to the fact that the given video has a bad quality and most 
of the faces appeared blurry (and very small). 


I have attached a zip file containing the final result (extracted_faces)

folders faces-1291,faces-1544 as well as several others gave some very good results

## DISCLAIMER:

the number attached to the faces folder are from the tracking ALGORITHM(i.e, the tracking ids are usually not in a consecutive order)
