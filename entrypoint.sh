#!/bin/bash

echo "Aguardando o banco de dados..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco de dados disponível!"

# Executa as migrations com manage.py
echo "Executando migrations..."
python manage.py migrate

# Inicia o Flask
echo "Iniciando o servidor Flask..."
exec flask run --host=0.0.0.0 --port=5000
