FROM quay.io/karmab/python:3.11-slim-bookworm

MAINTAINER Karim Boumedhel <karimboumedhel@gmail.com>

LABEL name="karmab/glpic" \
      maintainer="karimboumedhel@gmail.com" \
      vendor="Karmalabs" \
      version="latest" \
      release="0" \
      summary="Glpi wrapper" \
      description="Glpi wrapper"

RUN mkdir /root/glpic
ADD glpic /root/glpic/glpic
COPY setup.py /root/glpic
RUN pip3 install --no-cache /root/glpic

ENTRYPOINT ["/usr/local/bin/glpic"]
CMD ["-h"]
