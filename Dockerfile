FROM python:3.10

RUN apt update; \
    apt install opencc vim -y; \
    apt clean

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY dist/bagbag-*.whl /tmp/
RUN pip install /tmp/bagbag-*.whl

WORKDIR /app

CMD ["python", "run.py"]