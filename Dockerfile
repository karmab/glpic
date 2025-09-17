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
ADD README.md /root/glpic
ADD src /root/glpic/src
COPY pyproject.toml /root/glpic
RUN pip3 install -U pip wheel build && pip3 install -e /root/glpic

ENTRYPOINT ["/usr/local/bin/glpic"]
CMD ["-h"]
