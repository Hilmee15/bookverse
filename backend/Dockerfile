# ============================================================
# BookVerse backend - MULTI-STAGE build
# Stage 1 (builder): install Python dependencies into a venv
# Stage 2 (runtime): slim image that only carries the venv + app
# ============================================================

# ---------- Stage 1: builder ----------
# Version-specific tag (NOT latest) -> reproducible builds
FROM python:3.12.7-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Copy ONLY the dependency manifest first, so Docker caches this
# layer and skips reinstalling deps when just the source changes.
COPY requirements.txt .

# Install dependencies into an isolated venv that we will copy
# to the runtime stage (this is what multi-stage is for).
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12.7-slim AS runtime

# Security: never run the app as root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Bring only the ready-made venv from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Application source copied AFTER dependencies (cache-friendly)
COPY app ./app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

# Document the listening port
EXPOSE 8000

# Exec form (JSON array): uvicorn runs as PID 1, receives signals
# directly -> graceful shutdown with `docker stop`.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
