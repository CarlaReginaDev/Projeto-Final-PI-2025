#!/bin/sh

# $DB_HOST e $DB_PORT são variáveis de ambiente passadas pelo docker-compose.yml
echo "Aguardando o PostgreSQL em $DB_HOST:$DB_PORT..."

# Loop até que a porta do DB esteja aberta
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL iniciado!"

# CORREÇÃO CRÍTICA: Adiciona o diretório /app (raiz do volume) ao PYTHONPATH.
# Isso permite que o Python encontre o módulo 'workapp' aninhado.
export PYTHONPATH=$PYTHONPATH:/app

# Execute as migrações do banco de dados
echo "Executando migrações..."
python workapp/manage.py makemigrations
python workapp/manage.py migrate

# Inicie o comando principal (o CMD do Dockerfile)
exec "$@"