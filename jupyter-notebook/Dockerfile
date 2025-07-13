ARG PYTHON_BASE=3.12-alpine
FROM python:${PYTHON_BASE}
ARG JUPYTER_VERSION=7.4.2
ARG CUSTOM_USER=jupyter

WORKDIR /

RUN apk add --no-cache gcc musl-dev linux-headers && \
	pip install --no-cache notebook==${JUPYTER_VERSION} jupyterlab-spreadsheet-editor==0.7.2 && \
	jupyter server extension disable jupyter_server_terminals && \
	wget https://raw.githubusercontent.com/imba-tjd/pip-autoremove/1c631f0a723517e10d9244102806aef33a9d9db2/pip_autoremove.py -O ./pip_autoremove.py && \
	python3 pip_autoremove.py -y ipykernel terminado debugpy setuptools && \
	pip uninstall -y pip && \
	apk del gcc musl-dev linux-headers && \
	rm -rf /var/cache /root/.cache ./pip_autoremove.py && \
	(find / -name __pycache__ | xargs rm -rf)

RUN sed -i 's/<head>/<head><link rel="stylesheet" type="text\/css" href="{{ base_url | escape }}custom\/custom.css"\/>/' \
	/usr/local/lib/python${PYTHON_VERSION%.*}/site-packages/notebook/templates/edit.html

RUN for jsFile in /usr/local/share/jupyter/labextensions/spreadsheet-editor/static/*.js; do \
		sed -i 's/this.fitMode="all-equal-default",e.localPath.endsWith/this.fitMode="all-equal-fit",e.localPath.endsWith/g' $jsFile; \
		sed -i 's/(this.fitMode="fit-cells",this.relayout())/(this.fitMode="all-equal-fit",this.relayout())/g' $jsFile; \
	done

RUN adduser --disabled-password --gecos "" ${CUSTOM_USER}

USER ${CUSTOM_USER}

WORKDIR /home/${CUSTOM_USER}

# Must be created by the custom user instead of root.
RUN mkdir .jupyter

COPY custom.css .jupyter/custom/custom.css
COPY jupyter_notebook_config.py .jupyter/jupyter_notebook_config.py

CMD ["jupyter", "notebook"]
