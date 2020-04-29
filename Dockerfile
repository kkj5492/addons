#ARG BUILD_FROM="alpine:latest"
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh makeconf.sh rs485.py /

# Install requirements for add-on
RUN apk add --no-cache jq
RUN apk add --no-cache python3 && \
	if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
	python -m pip install pyserial && \
	python -m pip install paho-mqtt

WORKDIR /share

RUN chmod a+x /makeconf.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
