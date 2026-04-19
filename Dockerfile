FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates \
    && pip install playwright==1.44.0 requests \
    && playwright install chromium \
    && playwright install-deps chromium \
    && apt-get clean

COPY . .

CMD ["python", "aviator_bot.py"]
