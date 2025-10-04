from fastapi import FastAPI, HTTPException
import redis
import os
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="N8N API - Thread Manager",
    description="API simples para gerenciar threads usando Redis",
    version="1.0.0"
)

# Configurar conexão com Redis
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

# Configurar cliente OpenAI
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.get("/")
def read_root():
    """Endpoint raiz para verificar se a API está funcionando"""
    return {"message": "API N8N Thread Manager está funcionando!"}

@app.get("/thread/{numero}")
def get_thread(numero: str) -> Dict[str, int | str]:
    """
    Endpoint para buscar ou criar uma thread OpenAI para um número específico.
    
    Args:
        numero: Número para o qual buscar/criar a thread
        
    Returns:
        Dict com o número original e o ID da thread OpenAI
    """
    try:
        # Chave no Redis para armazenar a thread do número
        redis_key = f"thread:{numero}"
        
        # Verificar se já existe uma thread para este número
        thread_existente = redis_client.get(redis_key)
        
        if thread_existente:
            # Se existe, retornar a thread existente
            return {
                "numero": numero,
                "thread": thread_existente
            }
        else:
            # Se não existe, criar uma nova thread usando OpenAI
            try:
                empty_thread = openai_client.beta.threads.create()
                thread_id = empty_thread.id
                
                # Salvar o ID da thread no Redis
                redis_client.set(redis_key, thread_id)
                
                return {
                    "numero": numero,
                    "thread": thread_id
                }
            except Exception as openai_error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao criar thread na OpenAI: {str(openai_error)}"
                )
            
    except redis.RedisError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao conectar com Redis: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Endpoint para verificar a saúde da API e conexão com Redis"""
    try:
        # Testar conexão com Redis
        redis_client.ping()
        return {
            "status": "healthy",
            "redis": "connected"
        }
    except redis.RedisError:
        return {
            "status": "unhealthy",
            "redis": "disconnected"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

