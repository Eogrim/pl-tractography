# Docker file for the tractography plugin app

FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/tractography"  VERSION="0.1"
COPY ["tractography", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN pip install -r requirements.txt                                     \
  && apt-get update                                                     \
  && apt-get install -y dcmtk                                           \
  && apt-get install -y git                                             \
  && git clone git@github.com:FNNDSC/scripts.git


CMD ["tractography.py", "--help"]