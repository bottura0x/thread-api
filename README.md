# N8N API - Thread Manager

API simples para gerenciar threads da OpenAI usando Redis como cache.

## 🚀 Funcionalidades

- **GET `/thread/{numero}`** - Busca ou cria uma thread OpenAI para um número específico
- **GET `/health`** - Health check da API e conexão com Redis
- **GET `/`** - Endpoint raiz para verificar status da API

## ⚙️ Configuração

### Variáveis de Ambiente Necessárias

```bash
# API Key da OpenAI (obrigatória)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Configurações do Redis (opcionais)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### Como obter a API Key da OpenAI

1. Acesse [platform.openai.com](https://platform.openai.com/)
2. Faça login na sua conta
3. Vá para "API Keys" no menu
4. Clique em "Create new secret key"
5. Copie a chave gerada

## 🐳 Executando com Docker

```bash
# 1. Configure a variável de ambiente
export OPENAI_API_KEY=sk-your-api-key-here

# 2. Inicie os serviços
docker-compose up -d

# 3. Teste a API
curl http://localhost:8000/health
```

## 💻 Executando Localmente

```bash
# 1. Instale as dependências
uv sync

# 2. Inicie o Redis
docker-compose up -d redis

# 3. Configure a variável de ambiente
export OPENAI_API_KEY=sk-your-api-key-here

# 4. Execute a API
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📋 Exemplos de Uso

### Buscar/Criar Thread

```bash
# Primeira chamada - cria nova thread na OpenAI
curl http://localhost:8000/thread/123
{
  "numero": 123,
  "thread": "thread_abc123xyz456"
}

# Segunda chamada - retorna thread existente do Redis
curl http://localhost:8000/thread/123
{
  "numero": 123,
  "thread": "thread_abc123xyz456"
}
```

### Health Check

```bash
curl http://localhost:8000/health
{
  "status": "healthy",
  "redis": "connected"
}
```

## 🔧 Tecnologias

- **FastAPI** - Framework web moderno
- **OpenAI SDK** - Para criação de threads
- **Redis** - Cache das threads
- **Docker** - Containerização
- **UV** - Gerenciador de dependências Python
