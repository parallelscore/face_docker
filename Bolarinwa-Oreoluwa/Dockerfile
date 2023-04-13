FROM orgoro/dlib-opencv-python:latest

RUN apt-get upgrade && apt-get update 


RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

