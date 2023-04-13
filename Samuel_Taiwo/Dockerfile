FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get install --reinstall -y build-essential
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y cmake

##open cv
RUN apt-get install -y libgl1-mesa-glx 
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6


ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app/face_extraction.py"]