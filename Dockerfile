FROM python:3.10-rc

COPY LICENSE README.md /
WORKDIR /app

ADD src/ .
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
