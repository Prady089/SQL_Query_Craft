FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . .

# seed demo database at build time (creates demo.db)
RUN python seed_db.py || true

EXPOSE 8000

# default to running the API backend (bind to 0.0.0.0 for container)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
