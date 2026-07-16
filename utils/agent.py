from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

SYSTEM_PROMPT = """Eres SENTINEL, el asistente inteligente de JJC para 
gestion de contratos y project controls en proyectos mineros EPC en Peru.

Respondes consultas basandote EXCLUSIVAMENTE en la siguiente documentacion 
oficial de JJC:

{contexto}

REGLAS:
1. Responde siempre en espanol
2. Cita el documento fuente cuando respondas
3. Si la informacion no esta en los documentos responde:
   Esta consulta esta fuera de mi base de conocimiento actual.
4. Para montos mayores a USD 80,000 agrega siempre:
   REQUIERE FIRMA HUMANA - Physical Key activo
5. Maximo 3 parrafos por respuesta
6. Tono profesional y tecnico"""

class AgenteSentinel:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1
        )
        self.historial = []

    def invoke(self, input_dict):
        pregunta = input_dict["question"]

        # Buscar documentos relevantes
        docs = self.vector_store.similarity_search(pregunta, k=4)
        contexto = "\n\n".join([doc.page_content for doc in docs])

        # Construir mensajes
        mensajes = [
            HumanMessage(content=SYSTEM_PROMPT.format(contexto=contexto))
        ]

        # Agregar historial reciente
        for msg in self.historial[-4:]:
            mensajes.append(msg)

        # Agregar pregunta actual
        mensajes.append(HumanMessage(content=pregunta))

        # Obtener respuesta
        respuesta = self.llm.invoke(mensajes)

        # Guardar en historial
        self.historial.append(HumanMessage(content=pregunta))
        self.historial.append(AIMessage(content=respuesta.content))

        return {
            "answer": respuesta.content,
            "source_documents": docs
        }

def crear_agente(vector_store):
    return AgenteSentinel(vector_store)
