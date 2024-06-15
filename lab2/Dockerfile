FROM python:3.8-slim

RUN apt-get update && apt-get install -y iputils-ping

COPY find_mtu.py /

ENTRYPOINT [ "python3", "./find_mtu.py" ]