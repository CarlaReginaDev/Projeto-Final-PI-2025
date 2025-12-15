# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Defina variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instale dependências do sistema (netcat)
# 'nc' (netcat) é usado pelo entrypoint.sh para verificar se o Postgres está pronto
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copie o resto do código do projeto para o diretório de trabalho
COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]


