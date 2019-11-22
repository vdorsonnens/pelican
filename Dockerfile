FROM alpine:3.8

RUN apk -U add --virtual build-deps gcc python-dev musl-dev \
    python3 \
    py-pip \
    postgresql-dev

RUN pip install setuptools

COPY . .

RUN python setup.py install

EXPOSE 8001

RUN chmod +x /samples/start.sh

CMD ["/bin/sh", "/samples/start.sh"]
