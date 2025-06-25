# Stage 1: The Builder
# This stage installs all the Python dependencies.
FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim
WORKDIR /app

RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser
COPY app.py .
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.headless=true", "--server.enableCORS=false", "--server.address=0.0.0.0"]
