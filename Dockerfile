FROM python:3.12-slim

WORKDIR /app

# (Опційно) щоб логи одразу були в консолі, без буферизації
ENV PYTHONUNBUFFERED=1

# Якщо буде requirements.txt — поставимо залежності
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Код
COPY src /app/src

# За замовчуванням запускаємо main.py
CMD ["python", "src/main.py"]
