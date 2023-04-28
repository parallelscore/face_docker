FROM python:3

RUN apt-get upgrade && apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install libxcb-xinerama0

RUN apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev -y

RUN apt-get install --upgrade pip -y

RUN apt update && apt install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "face_detect.py" ]

# To run the docker file

# docker build -t face_detect .
# docker run face_detect
