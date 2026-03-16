FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base AS runtime

COPY . .

EXPOSE 18000

CMD ["sh", "-c", "python -m app.init_db && gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:18000 --workers 2 --access-logfile - --error-logfile -"]
