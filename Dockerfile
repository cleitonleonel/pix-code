# Imagem base
FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc && \
    apt-get install -y cairo libpango1.0-0 libgdk-pixbuf2.0-0 libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências do Python
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --with dev

# Copia o código
COPY . .

# Comando padrão
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
