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
    page_icon="🛡️",
    layout="wide"
)

# ── Session State ────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "tema" not in st.session_state:
    st.session_state.tema = "oscuro"

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

if "agente" not in st.session_state:
    with st.spinner("Cargando base de conocimiento JJC..."):
        vs = cargar_o_crear_vector_store()
        st.session_state.agente = crear_agente(vs)

# ── Textos según idioma ───────────────────────────────────────────────────────
TEXTOS = {
    "Español": {
        "titulo": "🛡️ SENTINEL — Mesa de Control Digital JJC",
        "subtitulo": "Agente IA para Contract Sentinel | Project Controls | Minería EPC Perú",
        "docs_header": "📋 Documentación disponible",
        "sesion": "Sesión",
        "nueva_conv": "🗑️ Nueva conversación",
        "preguntas_ejemplo": "**Preguntas de ejemplo:**",
        "ejemplos": [
            "¿Qué hace el Circuit Breaker?",
            "¿Cuál es el umbral del DQI para Modo Delegado?",
            "¿Cuántos sub-agentes tiene Contract Sentinel?",
            "¿Qué pasa con adicionales mayores a USD 80,000?",
            "Explica el Shadow Mode",
        ],
        "input_placeholder": "Consulta a SENTINEL...",
        "procesando": "SENTINEL procesando...",
        "fuentes": "Fuentes",
        "instruccion_idioma": "Responde siempre en español.",
    },
    "English": {
        "titulo": "🛡️ SENTINEL — JJC Digital Control Mesa",
        "subtitulo": "AI Agent for Contract Sentinel | Project Controls | EPC Mining Peru",
        "docs_header": "📋 Available documentation",
        "sesion": "Session",
        "nueva_conv": "🗑️ New conversation",
        "preguntas_ejemplo": "**Example questions:**",
        "ejemplos": [
            "What does the Circuit Breaker do?",
            "What is the DQI threshold for Delegated Mode?",
            "How many sub-agents does Contract Sentinel have?",
            "What happens with change orders over USD 80,000?",
            "Explain Shadow Mode",
        ],
        "input_placeholder": "Ask SENTINEL...",
        "procesando": "SENTINEL processing...",
        "fuentes": "Sources",
        "instruccion_idioma": "Always answer in English.",
    },
}

# ── Sidebar: controles de tema e idioma ──────────────────────────────────────
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌗 Tema"):
            st.session_state.tema = "claro" if st.session_state.tema == "oscuro" else "oscuro"
            st.rerun()
    with col2:
        idioma_sel = st.selectbox(
            "🌐",
            ["Español", "English"],
            index=["Español", "English"].index(st.session_state.idioma),
            label_visibility="collapsed"
        )
        if idioma_sel != st.session_state.idioma:
            st.session_state.idioma = idioma_sel
            st.rerun()

t = TEXTOS[st.session_state.idioma]

# ── Aplicar tema ──────────────────────────────────────────────────────────────
if st.session_state.tema == "claro":
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #1A1A1A; }
        [data-testid="stHeader"] { background-color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #F0F2F6; }
        [data-testid="stSidebar"] * { color: #1A1A1A !important; }
        [data-testid="stSidebar"] button {
            background-color: #FFFFFF !important;
            border: 1px solid #CCCCCC !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #E0E0E0 !important;
            border: 1px solid #999999 !important;
        }
        [data-testid="stSelectbox"] > div > div {
            background-color: #FFFFFF !important;
            border: 1px solid #CCCCCC !important;
        }
        [data-testid="stSelectbox"] * {
            color: #1A1A1A !important;
        }
        [data-testid="stChatMessage"] { background-color: #F0F2F6 !important; }
        [data-testid="stChatMessage"] p { color: #1A1A1A !important; }
        [data-testid="stCaptionContainer"] { color: #444444 !important; }
        [data-testid="stMarkdownContainer"] { color: #1A1A1A !important; }
        [data-testid="stMarkdownContainer"] li { color: #1A1A1A !important; }
        [data-testid="stBottomBlockContainer"] { background-color: #FFFFFF !important; }
        [data-testid="stBottom"] { background-color: #FFFFFF !important; }
        [data-testid="stChatInput"],
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] div {
            background-color: #F0F2F6 !important;
        }
        [data-testid="stChatInput"] textarea {
            background-color: #F0F2F6 !important;
            color: #1A1A1A !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #666666 !important;
        }
        [data-baseweb="select"] { background-color: #FFFFFF !important; }
        [data-baseweb="select"] * { color: #1A1A1A !important; }
        h1, h2, h3, p, span, label { color: #1A1A1A !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        [data-testid="stSidebar"] { background-color: #1A1D24; }
        </style>
    """, unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.title(t["titulo"])
st.caption(t["subtitulo"])
st.divider()

# ── Sidebar: documentación y ejemplos ────────────────────────────────────────
with st.sidebar:
    st.header(t["docs_header"])
    st.markdown("""
    - **DOC-01** Board Recommendation
    - **DOC-02** Executive Summary
    - **DOC-03** Framework AgentOps y DQI
    - **DOC-04** Arquitectura Contract Sentinel
    - **DOC-05** Mapa de Umbrales y Salvaguardas
    """)

    st.divider()
    st.caption(f"{t['sesion']}: `{st.session_state.session_id}`")

    if st.button(t["nueva_conv"]):
        st.session_state.mensajes = []
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.rerun()

    st.divider()
    st.markdown(t["preguntas_ejemplo"])
    for ej in t["ejemplos"]:
        if st.button(ej, key=ej):
            st.session_state.pregunta_ejemplo = ej

# ── Historial de chat ────────────────────────────────────────────────────────
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input del usuario ────────────────────────────────────────────────────────
pregunta = st.chat_input(t["input_placeholder"])

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
        with st.spinner(t["procesando"]):
            pregunta_con_idioma = f"{pregunta}\n\n({t['instruccion_idioma']})"
            resultado = st.session_state.agente.invoke(
                {"question": pregunta_con_idioma}
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
                st.caption(f"{t['fuentes']}: {', '.join(fuentes)}")

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
