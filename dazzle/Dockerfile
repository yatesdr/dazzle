FROM python:3.11-alpine as compile-image
RUN apk add --virtual mybuild cmake alsa-lib-dev gcc rust curl cargo build-base
RUN apk add alsa-utils ffmpeg py3-simpleaudio

# Build into venv
RUN python3 -mvenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install pydub lpminimk3 simpleaudio

# Build running image
FROM python:3.11-alpine AS build-image
RUN apk add alsa-utils ffmpeg py3-simpleaudio
COPY --from=compile-image /opt/venv /opt/venv
COPY . /app/
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
ENTRYPOINT ["python3","app.py"]
