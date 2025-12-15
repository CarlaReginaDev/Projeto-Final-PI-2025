#!/bin/sh


echo "Aguardando o PostgreSQL..."

# Loop até que a porta do DB esteja aberta
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL iniciado!"

# CORREÇÃO CRÍTICA: Adiciona o diretório /app (raiz do volume) ao PYTHONPATH.
# Isso permite que o Python encontre o módulo 'workapp' aninhado.
export PYTHONPATH=$PYTHONPATH:/app

# Execute as migrações do banco de dados
echo "Executando migrações..."
python workapp/manage.py migrate

# Inicie o comando principal (o CMD do Dockerfile)
echo "Iniciando servidor Django..."
python workapp/manage.py runserver 0.0.0.0:8000