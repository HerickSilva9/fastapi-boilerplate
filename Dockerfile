# ---- Base Stage ----
FROM python:3.12.3 AS base

WORKDIR /app

# Install UV (dependency manager)
COPY --from=ghcr.io/astral-sh/uv:0.7.22 /uv /uvx /bin/

# Configure environment variables
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH=/app UV_LINK_MODE=copy

# Copy dependency files and install project dependencies
COPY ./pyproject.toml ./uv.lock /app/
RUN uv sync --locked --no-dev


# ---- Development & Tests Stage ----
FROM base AS dev

# Install development dependencies
RUN uv sync --locked --dev

# Copy source code and tests into the container and run default command
COPY ./app /app/app
COPY ./tests /app/tests
CMD ["python", "-m", "pytest", "--cov=app", "--cov-report=term-missing"]


# ---- Production Stage ----
FROM base AS production

# Copy application source code and run the application
COPY ./app /app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]