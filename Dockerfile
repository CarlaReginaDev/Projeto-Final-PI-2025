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

# Copie o script de entrypoint e dê permissão de execução
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copie o resto do código do projeto para o diretório de trabalho
COPY . .

RUN python WorkApp/manage.py makemigrations
RUN python WorkApp/manage.py migrate

# O entrypoint será executado primeiro
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "WorkApp/manage.py", "runserver", "0.0.0.0:8000"]
