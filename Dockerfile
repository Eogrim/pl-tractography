# Docker file for the tractography plugin app

FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/tractography"  VERSION="0.1"
COPY ["tractography", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN pip install -r requirements.txt                                     \
  && apt-get update                                                     \
  && apt-get install dcmtk                                              


CMD ["tractography.py", "--help"]