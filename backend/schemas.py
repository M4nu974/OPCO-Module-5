import time
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union

# --- Modèles pour la Requête (Request) ---

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "codegen-finetuned"
    messages: List[ChatMessage]

# --- Modèles pour la Réponse (Response) ---

class Choice(BaseModel):
    index: int = 0
    message: ChatMessage

class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{''.join(str(time.time()).split('.'))}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[Choice]

