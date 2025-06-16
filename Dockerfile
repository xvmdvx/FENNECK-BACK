FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["bash", "start.sh"]
