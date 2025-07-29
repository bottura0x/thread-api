FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar uv para gerenciamento de dependências
RUN pip install uv

# Copiar arquivos de configuração
COPY pyproject.toml uv.lock ./

# Instalar dependências
RUN uv sync --frozen

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 