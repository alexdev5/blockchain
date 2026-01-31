FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY src /app/src
EXPOSE 5000
CMD ["python", "src/main.py"]
