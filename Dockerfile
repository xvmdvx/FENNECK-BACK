FROM python:3.11-slim

WORKDIR /app

# default rules file location
ENV RULES_FILE=Bizee_rules.txt

COPY requirements.txt .
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["bash", "start.sh"]
