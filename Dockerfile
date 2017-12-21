FROM python:3
MAINTAINER Haha People Maintain Software?

RUN apt-get update
RUN apt-get install -y libenchant1c2a

RUN useradd -m -d /home/sopel sopel
WORKDIR /home/sopel

RUN pip install git+https://github.com/sopel-irc/sopel.git

VOLUME /home/sopel/.sopel
RUN mkdir /home/sopel/.sopel/modules

COPY crypto.py /home/sopel/.sopel/modules/

USER sopel
CMD sopel
