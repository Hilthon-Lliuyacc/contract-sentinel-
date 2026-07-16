import streamlit as st
from dotenv import load_dotenv
from utils.vector_store import cargar_o_crear_vector_store
from utils.agent import crear_agente
from utils.db import guardar_conversacion
import uuid
import os

load_dotenv()

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="SENTINEL — JJC Contract Intelligence",
    page_icon="🏗️",
    layout="wide"
)

# ── Session State ────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "agente" not in st.session_state:
    with st.spinner("Cargando base de conocimiento JJC..."):
        vs = cargar_o_crear_vector_store()
        st.session_state.agente = crear_agente(vs)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🏗️ SENTINEL — Mesa de Control Digital JJC")
st.caption("Agente IA para Contract Sentinel | Project Controls | Mineria EPC Peru")
st.divider()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Documentacion disponible")
    st.markdown("""
    - **DOC-01** Board Recommendation
    - **DOC-02** Executive Summary
    - **DOC-03** Framework AgentOps y DQI
    - **DOC-04** Arquitectura Contract Sentinel
    - **DOC-05** Mapa de Umbrales y Salvaguardas
    """)

    st.divider()
    st.caption(f"Sesion: `{st.session_state.session_id}`")

    if st.button("🗑️ Nueva conversacion"):
        st.session_state.mensajes = []
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.rerun()

    st.divider()
    st.markdown("**Preguntas de ejemplo:**")
    ejemplos = [
        "Que hace el Circuit Breaker?",
        "Cual es el umbral del DQI para Modo Delegado?",
        "Cuantos sub-agentes tiene Contract Sentinel?",
        "Que pasa con adicionales mayores a USD 80,000?",
        "Explica el Shadow Mode",
    ]
    for ej in ejemplos:
        if st.button(ej, key=ej):
            st.session_state.pregunta_ejemplo = ej

# ── Historial de chat ────────────────────────────────────────────────────────
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input del usuario ────────────────────────────────────────────────────────
pregunta = st.chat_input("Consulta a SENTINEL...")

if "pregunta_ejemplo" in st.session_state:
    pregunta = st.session_state.pregunta_ejemplo
    del st.session_state.pregunta_ejemplo

if pregunta:
    st.session_state.mensajes.append({
        "role": "user",
        "content": pregunta
    })
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("SENTINEL procesando..."):
            resultado = st.session_state.agente.invoke(
                {"question": pregunta}
            )
            respuesta = resultado["answer"]

            fuentes = []
            if "source_documents" in resultado:
                for doc in resultado["source_documents"]:
                    nombre = doc.metadata.get("source", "")
                    if nombre and nombre not in fuentes:
                        fuentes.append(
                            os.path.basename(nombre)
                        )

            st.markdown(respuesta)

            if fuentes:
                st.caption(f"Fuentes: {', '.join(fuentes)}")

    fuentes_str = ", ".join(fuentes) if fuentes else ""
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": respuesta
    })
    guardar_conversacion(
        st.session_state.session_id,
        pregunta,
        respuesta,
        fuentes_str
    )