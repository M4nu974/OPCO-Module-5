import pytest

# On importe les objets réels depuis votre application
from backend.main import inference, tokenizer, model


def test_inference_returns_string():
    # 1. Préparation d'un prompt simple
    prompt = "Dis bonjour"

    # 2. Appel de la vraie fonction d'inférence
    # Cette étape va prendre du temps car elle fait appel au modèle.
    result = inference(prompt, tokenizer, model)

    # 3. Vérification du type de la réponse
    # On s'assure que le résultat est bien une chaîne de caractères (str).
    assert isinstance(result, str)

    # On peut aussi vérifier qu'elle n'est pas vide.
    assert result != ""

