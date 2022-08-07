FROM python:3

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt; \
    apt update; \
    apt install opencc -y; \
    apt clean

COPY dist/bagbag-*.whl /tmp/
RUN pip install /tmp/bagbag-*.whl

WORKDIR /app

CMD ["python", "run.py"]