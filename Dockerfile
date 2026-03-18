FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Se usa camoufox, mantém:
RUN camoufox fetch || true

COPY . .

CMD ["python", "app.py"]
