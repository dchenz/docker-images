FROM python:3.12-slim

ARG CERTBOT_VERSION

RUN apt update && apt install -y libaugeas0

RUN pip install certbot==${CERTBOT_VERSION}

ENTRYPOINT ["certbot"]
