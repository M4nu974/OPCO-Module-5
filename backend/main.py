import time

import torch
from fastapi import FastAPI, Request
from loguru import logger
from transformers import AutoTokenizer, AutoModelForCausalLM
from backend.schemas import ChatCompletionRequest, ChatCompletionResponse, ChatMessage, Choice
from backend.modules.calcul import inference

# --- Configuration de l'application ---
MODEL_PATH = "Salesforce/codegen-350M-mono"
app = FastAPI(
    title="API d'inférence type OpenAI",
    description="Une API compatible avec la structure de requêtes/réponses d'OpenAI pour un modèle CodeGen.",
    version="1.0.0",
)

# --- Collection des métriques ---
metrics = {
    "requests_total": 0,
    "errors_total": 0,
    "total_response_time_ms": 0.0,
    "average_response_time_ms": 0.0,
}

# Middleware pour intercepter les requêtes et collecter les métriques
@app.middleware("http")
async def collect_metrics_middleware(request: Request, call_next):
    # Ignore les requêtes vers les endpoints de métriques et de santé
    if request.url.path in ["/metrics", "/health"]:
        return await call_next(request)

    start_time = time.time()

    try:
        response = await call_next(request)
        # Compte les erreurs serveur (status code 500 ou plus)
        if response.status_code >= 500:
            metrics["errors_total"] += 1
    except Exception:
        metrics["errors_total"] += 1
        raise

    process_time_ms = (time.time() - start_time) * 1000

    # Mise à jour des métriques
    metrics["requests_total"] += 1
    metrics["total_response_time_ms"] += process_time_ms
    metrics["average_response_time_ms"] = metrics["total_response_time_ms"] / metrics["requests_total"]

    logger.info(f"Request to {request.url.path} completed in {process_time_ms:.2f}ms")

    return response

logger.info(f"Chargement du modèle depuis : {MODEL_PATH}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16  # Assurez-vous que votre hardware supporte le float16
)
logger.info("Modèle chargé avec succès.")

# --- Endpoints de l'API ---
@app.get("/metrics")
async def get_metrics():
    return metrics

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", summary="Endpoint de statut")
async def root():
    return {"message": "L'API est fonctionnelle. Utilisez l'endpoint POST /api/v1/chat/completions pour l'inférence."}

@app.post(
    "/api/v1/chat/completions",
    response_model=ChatCompletionResponse,
    summary="Générer une complétion de chat"
)
async def create_chat_completion(request: ChatCompletionRequest):
    # 1. Extraire le contenu du message utilisateur
    user_message = next((msg.content for msg in reversed(request.messages) if msg.role == 'user'), None)

    if not user_message:
        return ChatCompletionResponse(
            model=request.model or MODEL_PATH,
            choices=[Choice(index=0, message=ChatMessage(role="assistant", content="Aucun message utilisateur trouvé."))]
        )

    # 2. On prépare le prompt pour le modèle
    system_prompt = "---"
    full_prompt = f"{system_prompt}\n{user_message}"
    logger.info(f"Début de l'inférence pour le prompt : '{user_message[:100]}...'")

    # 3. On appelle la fonction d'inférence
    raw_response = inference(
        full_prompt,
        tokenizer,
        model
    )
    logger.info("Inférence terminée.")

    # 4. Nettoyer la réponse
    cleaned_response = raw_response.split("---")[-1].strip()

    # 5. Construire l'objet de réponse Pydantic
    response_message = ChatMessage(role="assistant", content=cleaned_response)
    choice = Choice(index=0, message=response_message)

    chat_response = ChatCompletionResponse(
        model=request.model or MODEL_PATH,
        choices=[choice]
    )

    return chat_response
