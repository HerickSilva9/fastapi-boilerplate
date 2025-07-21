FROM python:3.12.3

# Definir diretório de trabalho
WORKDIR /app

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:0.7.22 /uv /uvx /bin/

# Configurar PATH para usar os binários do venv
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_LINK_MODE=copy

# Copiar arquivos de dependências
COPY ./pyproject.toml ./uv.lock /app/

# Instalar dependências
RUN uv sync --locked

# Definir PYTHONPATH para o app
ENV PYTHONPATH=/app

# Copiar o restante do código
COPY ./app /app/app
COPY ./tests /app/tests

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]