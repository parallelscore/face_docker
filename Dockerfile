FROM python:3.7


WORKDIR /home/user
COPY . /home/user/

RUN run.sh


CMD ["python", "app.py" ]


