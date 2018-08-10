# Docker file for the tractography plugin app

FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/tractography"  VERSION="0.1"
COPY ["tractography", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN pip install -r requirements.txt										\
  && apt-get update                                                     \
  && apt-get install sudo                                               \
  && useradd -u $UID -ms /bin/bash localuser                            \
  && addgroup localuser sudo                                            \
  && echo "localuser:localuser" | chpasswd                              \
  && adduser localuser sudo                                             \
  && apt-get install dcmtk				                                \


CMD ["tractography.py", "--help"]