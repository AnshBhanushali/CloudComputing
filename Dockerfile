FROM python:3.9-alpine

WORKDIR /app

COPY scripts/scripts.py /app/scripts.py

COPY home/data /home/data

RUN mkdir -p /home/data/output && chmod -R 755 /home/data

CMD ["python", "scripts.py"]
