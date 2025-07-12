ARG PYTHON_BASE=3.12-alpine

FROM python:${PYTHON_BASE}

ARG CUSTOM_USER=abcdef
ARG _APK_PACKAGES="gcc musl-dev linux-headers"
ARG _PIP_PACKAGES="ipykernel terminado debugpy"
ARG JUPYTER_VERSION=7.4.2

WORKDIR /

RUN apk add --no-cache ${_APK_PACKAGES} && \
	pip install --no-cache-dir notebook==${JUPYTER_VERSION} && \
	jupyter server extension disable jupyter_server_terminals && \
	pip uninstall -y ${_PIP_PACKAGES} && \
	apk del ${_APK_PACKAGES} && \
	rm -rf /root/.cache && \
	(find / -name __pycache__ | xargs rm -rf)

# HACK: I want custom.css to load when editing a notebook.
RUN sed -i 's/<head>/<head><link rel="stylesheet" type="text\/css" href="{{ base_url | escape }}custom\/custom.css"\/>/' \
	/usr/local/lib/python${PYTHON_VERSION%.*}/site-packages/notebook/templates/edit.html

RUN adduser --disabled-password --gecos "" ${CUSTOM_USER}

USER ${CUSTOM_USER}

WORKDIR /home/${CUSTOM_USER}

# Must be created by the cutom user instead of root.
RUN mkdir .jupyter

COPY custom.css .jupyter/custom/custom.css

CMD ["jupyter", "notebook"]
