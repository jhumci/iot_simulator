# syntax=docker/dockerfile:1.4
FROM python:3 AS builder

WORKDIR /iot_simulator

COPY requirements.txt /iot_simulator
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /iot_simulator

ENTRYPOINT ["python3"]
#CMD ["main.py"]

# Use a shell command to loop and restart the Python script
CMD ["sh", "-c", "while true; do python3 main.py; sleep 1; done"]

FROM builder as dev-envs

