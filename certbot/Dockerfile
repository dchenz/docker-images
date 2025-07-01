FROM python:3.12-slim

RUN apt update && apt install -y libaugeas0

RUN pip install certbot==3.3.0

ENTRYPOINT ["certbot"]
