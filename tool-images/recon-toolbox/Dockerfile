FROM golang:1.23-alpine AS build

RUN apk add --no-cache git build-base

RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install -v github.com/OJ/gobuster/v3@latest

# Pre-bakea los templates de nuclei en la imagen para que los jobs no dependan
# de descargarlos en cada ejecución (los contenedores corren con filesystem
# read-only salvo /tmp).
RUN /root/go/bin/nuclei -update-templates -silent || true

FROM alpine:3.20

RUN apk add --no-cache ca-certificates nmap nmap-scripts ruby ruby-json git && \
    addgroup -S scanner && adduser -S scanner -G scanner && \
    git clone --depth 1 https://github.com/urbanadventurer/WhatWeb.git /opt/whatweb && \
    printf '#!/bin/sh\nexec ruby /opt/whatweb/whatweb "$@"\n' > /usr/local/bin/whatweb && \
    chmod +x /usr/local/bin/whatweb

COPY --from=build /root/go/bin/subfinder /usr/local/bin/subfinder
COPY --from=build /root/go/bin/httpx /usr/local/bin/httpx
COPY --from=build /root/go/bin/nuclei /usr/local/bin/nuclei
COPY --from=build /root/go/bin/gobuster /usr/local/bin/gobuster
COPY --from=build /root/nuclei-templates /home/scanner/nuclei-templates
COPY wordlists/common.txt /home/scanner/wordlists/common.txt

ENV HOME=/home/scanner
RUN chown -R scanner:scanner /home/scanner /opt/whatweb

USER scanner
WORKDIR /home/scanner

ENTRYPOINT []
