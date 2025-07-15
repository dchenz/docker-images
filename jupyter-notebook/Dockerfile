ARG PYTHON_BASE=3.12-alpine

FROM python:${PYTHON_BASE} AS jse_builder

RUN apk add gcc git musl-dev linux-headers nodejs

RUN pip install --break-system-packages git+https://github.com/dchenz/jupyterlab-spreadsheet-editor.git@0ea1aba2cd8b2d672ace220b27395855af12bb8b && \
	(find / -name __pycache__ | xargs rm -rf)

FROM python:${PYTHON_BASE}

ARG JUPYTER_VERSION=7.4.2
ARG CUSTOM_USER=jupyter

WORKDIR /

RUN apk add --no-cache gcc musl-dev linux-headers && \
	pip install --no-cache notebook==${JUPYTER_VERSION} && \
	jupyter server extension disable jupyter_server_terminals && \
	wget https://raw.githubusercontent.com/imba-tjd/pip-autoremove/1c631f0a723517e10d9244102806aef33a9d9db2/pip_autoremove.py -O ./pip_autoremove.py && \
	python3 pip_autoremove.py -y ipykernel terminado debugpy setuptools && \
	pip uninstall -y pip && \
	apk del gcc musl-dev linux-headers && \
	rm -rf /var/cache /root/.cache ./pip_autoremove.py && \
	(find / -name __pycache__ | xargs rm -rf)

RUN sed -i 's/<head>/<head><link rel="stylesheet" type="text\/css" href="{{ base_url | escape }}custom\/custom.css"\/>/' \
	/usr/local/lib/python${PYTHON_VERSION%.*}/site-packages/notebook/templates/edit.html

# pip install git+https://github.com/dchenz/jupyterlab-spreadsheet-editor.git
COPY --from=jse_builder /usr/local/share/jupyter/labextensions/spreadsheet-editor /usr/local/share/jupyter/labextensions/spreadsheet-editor
COPY --from=jse_builder /usr/local/lib/python3.12/site-packages/jupyterlab_spreadsheet_editor /usr/local/lib/python3.12/site-packages/jupyterlab_spreadsheet_editor
COPY --from=jse_builder /usr/local/lib/python3.12/site-packages/jupyterlab_spreadsheet_editor-0.7.2.dist-info /usr/local/lib/python3.12/site-packages/jupyterlab_spreadsheet_editor-0.7.2.dist-info

RUN adduser --disabled-password --gecos "" ${CUSTOM_USER}

USER ${CUSTOM_USER}

WORKDIR /home/${CUSTOM_USER}

# Must be created by the custom user instead of root.
RUN mkdir .jupyter

COPY custom.css .jupyter/custom/custom.css
COPY jupyter_notebook_config.py .jupyter/jupyter_notebook_config.py

CMD ["jupyter", "notebook"]
