FROM python:3

RUN apt-get upgrade && apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install libxcb-xinerama0

RUN apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev -y

RUN python -m pip install --upgrade pip

# RUN apt-get install qt5-default -y

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "face_detect.py" ]

# docker build -t face_detect .
# docker run face_detect --youtube="https://youtu.be/JriaiYZZhbY"