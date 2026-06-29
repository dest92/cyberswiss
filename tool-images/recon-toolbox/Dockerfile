FROM golang:1.23-alpine AS build

RUN apk add --no-cache git build-base

RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Pre-bakea los templates de nuclei en la imagen para que los jobs no dependan
# de descargarlos en cada ejecución (los contenedores corren con filesystem
# read-only salvo /tmp).
RUN /root/go/bin/nuclei -update-templates -silent || true

FROM alpine:3.20

RUN apk add --no-cache ca-certificates && \
    addgroup -S scanner && adduser -S scanner -G scanner

COPY --from=build /root/go/bin/subfinder /usr/local/bin/subfinder
COPY --from=build /root/go/bin/httpx /usr/local/bin/httpx
COPY --from=build /root/go/bin/nuclei /usr/local/bin/nuclei
COPY --from=build /root/nuclei-templates /home/scanner/nuclei-templates

ENV HOME=/home/scanner
RUN chown -R scanner:scanner /home/scanner

USER scanner
WORKDIR /home/scanner

ENTRYPOINT []
