# https://github.com/linuxserver/docker-calibre-web

FROM ghcr.io/linuxserver/unrar:7.1.8 AS unrar

FROM ghcr.io/linuxserver/baseimage-ubuntu:noble

ARG CALIBRE_VERSION

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-pip && \
    apt-get install -y --no-install-recommends imagemagick ghostscript libmagic1t64 libxi6 libxslt1.1 python3-venv sqlite3 xdg-utils && \
    curl -o /tmp/calibre-web.tar.gz -L https://github.com/dchenz/calibre-web/archive/${CALIBRE_VERSION}.tar.gz && \
    mkdir -p /app/calibre-web && \
    tar xf /tmp/calibre-web.tar.gz -C /app/calibre-web --strip-components=1 && \
    cd /app/calibre-web && \
    pip install -U --no-cache-dir --break-system-packages --find-links https://wheel-index.linuxserver.io/ubuntu/ -r requirements.txt && \
    curl -o /usr/bin/kepubify -L https://github.com/pgaskin/kepubify/releases/download/v4.0.4/kepubify-linux-64bit && \
    cd /tmp && \
    curl -o docker-calibre-web.tar.gz -L https://github.com/linuxserver/docker-calibre-web/archive/refs/tags/0.6.24-ls339.tar.gz && \
    tar xf docker-calibre-web.tar.gz --strip-components=1 && \
    cp -r root/* / && \
    apt-get -y purge build-essential python3-pip && \
    apt-get -y autoremove && \
    rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/* /root/.cache && \
    (find / -name __pycache__ | xargs rm -rf)

COPY --from=unrar /usr/bin/unrar-ubuntu /usr/bin/unrar
