FROM python:3.6-stretch
LABEL maintainer="Michal Franczyk <mr.franczyk@gmail.com>"

WORKDIR ./app
COPY ./requirements.txt ./app/
RUN apt-get update 
RUN pip3 install pymongo bs4 requests flask-restful
COPY ./ ./app

CMD bash -c "while true; do sleep 30; done"
