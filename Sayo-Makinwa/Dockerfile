# FROM python:3.9-alpine
FROM civisanalytics/datascience-python:latest
# RUN apk add --no-cache py3-numpy

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get update && apt-get -y install cmake protobuf-compiler

RUN python -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]