FROM --platform=linux/arm64 python:3.9-bullseye

ARG NUITKA_VERSION=4.3
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python3.9 -m pip install "nuitka==${NUITKA_VERSION}"

COPY docker/build.sh /usr/local/bin/build-q2.sh
RUN chmod +x /usr/local/bin/build-q2.sh

WORKDIR /src
ENTRYPOINT ["/usr/local/bin/build-q2.sh"]
