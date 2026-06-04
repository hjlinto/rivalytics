# Rivalytics backend container
FROM python:3.13-slim

WORKDIR /app

# Install Python dependencies first for better Docker layer caching.
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code.
COPY backend ./backend

EXPOSE 8000

# Run FastAPI from the repo-style package path.
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]