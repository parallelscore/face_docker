FROM python:3.11.0

RUN apt-get update && apt-get --yes install libgl1

COPY . /app/src/
WORKDIR /app/src

RUN pip install --upgrade pip
RUN pip install https://download.pytorch.org/whl/cpu/torch-2.0.0%2Bcpu-cp311-cp311-linux_x86_64.whl
RUN pip install https://download.pytorch.org/whl/cpu/torchvision-0.15.1%2Bcpu-cp311-cp311-linux_x86_64.whl
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
