import streamlit as st
import requests

API_BASE_URL = "http://localhost:8001"

st.set_page_config(
    page_title="Interface pour API CodeGen",
    page_icon="🤖",
    layout="wide"
)

# --- BARRE DE NAVIGATION LATÉRALE ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisissez une page :",
    ("Chat Coder", "Tableau de Bord")
)

# --- AFFICHAGE DE LA PAGE SÉLECTIONNÉE ---

if page == "Chat Coder":
    st.title("🤖 Interface de complétion de code")

    # Zone de texte pour le prompt de l'utilisateur
    prompt_text = st.text_area("Entrez votre instruction ou votre début de code ici :", height=150)

    if st.button("Générer la suite"):
        if prompt_text:
            with st.spinner("Chargement de la réponse..."):
                # 1. Préparer la requête pour l'API
                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt_text
                        }
                    ]
                }
                api_endpoint = f"{API_BASE_URL}/api/v1/chat/completions"

                try:
                    # 2. Envoyer la requête à l'API FastAPI
                    response = requests.post(api_endpoint, json=payload)
                    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

                    # 3. Traiter la réponse
                    data = response.json()

                    # Extraire le contenu du message de l'assistant
                    if data.get("choices") and len(data["choices"]) > 0:
                        assistant_message = data["choices"][0]["message"]["content"]

                        st.subheader("Réponse du modèle :")
                        st.code(assistant_message, language='python', line_numbers=True)
                    else:
                        st.error("La réponse de l'API est dans un format inattendu.")
                        st.json(data)

                except requests.exceptions.RequestException as e:
                    st.error(f"Erreur de connexion à l'API : {e}")
                    st.info("Assurez-vous que le serveur FastAPI (main.py) est bien lancé sur l'adresse http://127.0.0.1:8001")
                except Exception as e:
                    st.error(f"Une erreur inattendue est survenue : {e}")


elif page == "Tableau de Bord":
    st.title("📊 Tableau de Bord de l'API")
    st.caption("Surveillance en temps réel de l'état et des métriques de l'API.")

    # --- HEALTH CHECK ---
    st.subheader("Vérification de l'état (Health Check)")
    status_placeholder = st.empty()

    def check_health():
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200 and response.json().get("status") == "ok":
                status_placeholder.success("✅ API en ligne et fonctionnelle.")
            else:
                status_placeholder.warning(f"⚠️ L'API a répondu avec un statut inattendu : {response.status_code}")
        except requests.exceptions.RequestException:
            status_placeholder.error("❌ API hors ligne ou inaccessible.")

    if st.button("Vérifier le statut de l'API"):
        check_health()

    st.divider()

    # --- AFFICHAGE DES MÉTRIQUES ---
    st.subheader("Métriques de Performance")

    if 'metrics' not in st.session_state:
        st.session_state.metrics = {"requests_total": 0, "errors_total": 0, "average_response_time_ms": 0.0}

    def get_metrics():
        try:
            response = requests.get(f"{API_BASE_URL}/metrics", timeout=5)
            response.raise_for_status()
            st.session_state.metrics = response.json()
        except requests.exceptions.RequestException:
            st.error("Impossible de récupérer les métriques.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Requêtes Totales", st.session_state.metrics["requests_total"])
    col2.metric("Erreurs Serveur", st.session_state.metrics["errors_total"])
    col3.metric("Temps de Réponse Moyen", f"{st.session_state.metrics['average_response_time_ms']:.2f} ms")

    if st.button("Rafraîchir les métriques"):
        get_metrics()

