FROM ubuntu:20.04

RUN apt update && apt-get install -y curl && apt-get install -y python3 && apt-get install -y python3-pip \
RUN python3 -m pip install virtualenv

MKDIR Projet_Linux_Image

WORKDIR /Projet_Linux_Image
COPY . .

RUN bash ../install.sh

CMD ["bash", "launch.sh"]