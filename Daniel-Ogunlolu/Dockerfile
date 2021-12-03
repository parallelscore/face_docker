FROM orgoro/dlib-opencv-python:latest
COPY .  /main
WORKDIR /main
RUN apt-get upgrade && apt-get update 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python extract-face.py
