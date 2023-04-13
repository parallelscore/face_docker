FROM ubuntu:latest

WORKDIR /app

COPY . /app

# apt-get update
RUN apt-get update -y

# tzdata
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Africa/Lagos
RUN apt-get install -y tzdata


# Install dependencies
RUN apt-get install -y \
    git \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    python3 \
    python3-pip \
    gcc \
    python3-tk \
    ffmpeg \
    libopenblas-dev \ 
    liblapack-dev

# Install dlib
RUN git clone https://github.com/davisking/dlib.git && \
    cd dlib && \
    mkdir build && \
    cd build && \
    cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 && \
    cmake --build . && \
    cd .. && \
    python3 setup.py install 

# Install Face Recognition and OpenCV
RUN pip3 install face_recognition opencv-python

# RUN apt-get upgrade && apt-get update
# RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "detect_unique_faces.py" ]