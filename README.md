# 🛡️ Contract Sentinel — Digital Control Mesa

**Arquitectura multiagente de IA para control de contratos EPC**, con validación financiera automática mediante un Circuit Breaker determinístico.

Desarrollado para el **Alura Agentic AI Challenge** por [Hilthon Lliuyacc León](https://github.com/Hilthon-Lliuyacc).

---

## 📋 ¿Qué es Contract Sentinel?

Contract Sentinel es un sistema de 7 agentes de IA que asiste en la gestión de contratos de proyectos EPC (Engineering, Procurement & Construction). Permite hacer **preguntas en lenguaje natural** sobre contratos, cláusulas, riesgos financieros y recomendaciones, mientras un motor de reglas independiente (**Circuit Breaker**) garantiza que ninguna acción financiera relevante se ejecute sin una validación humana.

> El código —no el modelo de lenguaje— decide qué acciones son permitidas. Esto asegura decisiones auditables, reversibles y seguras.

---

## 💬 Cómo hacer preguntas al agente

Una vez la aplicación está corriendo, puedes escribir tus preguntas directamente en el chat, en español, como si hablaras con un especialista en control de contratos. Algunos ejemplos:

```
¿Qué hace el Circuit Breaker?
¿Cuáles son los umbrales financieros definidos para este contrato?
Dame un resumen ejecutivo del contrato principal
¿Qué riesgos identifica el framework de AgentOps?
¿Qué acciones requieren firma digital humana?
Explícame la arquitectura de los 7 agentes
```

El agente responde citando siempre la fuente documental de donde extrajo la información (por ejemplo: *Fuente: Documento DOC-04 de JJC*), para que toda respuesta sea trazable.

### 📸 Ejemplo de uso

![Ejemplo de consulta al agente](screenshots/Captura%20de%20pantalla%202026-07-16%20084247.png)

*Pregunta al agente sobre el funcionamiento del Circuit Breaker, con respuesta citando las fuentes documentales correspondientes.*

---

## 🏗️ Arquitectura

El sistema está compuesto por 7 agentes especializados que trabajan sobre una base documental indexada (FAISS) y una capa de reglas de seguridad (Circuit Breaker):

| Componente | Función |
|---|---|
| **Agente conversacional** | Interpreta la pregunta del usuario y decide qué información buscar |
| **Vector store (FAISS)** | Búsqueda semántica sobre los documentos del contrato |
| **Circuit Breaker** | Valida cada acción propuesta contra umbrales financieros definidos; bloquea ejecución sin firma humana |
| **Base de datos** | Persistencia de contratos, umbrales y trazabilidad de decisiones |

---

## 📂 Estructura del proyecto

```
sentinel/
├── app.py                  # Aplicación principal
├── database/
│   └── schema.sql           # Esquema de base de datos
├── docs/                    # Documentación técnica y de negocio (JJC)
│   ├── 1_Board_Recommendation_Contract_Sentinel_JJC.pdf
│   ├── 2_Executive_Summary_Contract_Sentinel_JJC.pdf
│   ├── 3_AgentOps_Framework_DQI_Manual_JJC.pdf
│   ├── 4_Arquitectura_Contract_Sentinel_JJC.pdf
│   └── 5_Threshold_Map_Safeguard_Guide_JJC.pdf
├── utils/
│   ├── agent.py              # Lógica del agente conversacional
│   ├── db.py                 # Conexión y consultas a base de datos
│   └── vector_store.py       # Indexación y búsqueda semántica (FAISS)
├── screenshots/               # Capturas de la aplicación en uso
└── requirements.txt
```

---

## ⚙️ Instalación y ejecución

```bash
# Clonar el repositorio
git clone https://github.com/Hilthon-Lliuyacc/contract-sentinel-.git
cd contract-sentinel-

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate      # En Windows
# source venv/bin/activate # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Crear un archivo .env con tus credenciales (API keys, conexión a base de datos, etc.)

# Ejecutar la aplicación
python app.py
```

---

## 🔒 Seguridad

- Ninguna acción financiera se ejecuta automáticamente: todas pasan por el Circuit Breaker
- Las credenciales (`.env`) y entornos virtuales (`venv/`) están excluidos del control de versiones
- Todas las decisiones quedan registradas para auditoría posterior

---

## 🛠️ Tecnologías utilizadas

- **Python** — lógica de agentes y aplicación
- **Claude API (Sonnet)** — motor conversacional
- **FAISS** — búsqueda vectorial semántica
- **SQL** — persistencia de datos y trazabilidad

---

## 👤 Autor

**Hilthon Lliuyacc León** — Senior Project Controller, JJC
15+ años de experiencia en cost control, gestión de contratos FIDIC/NEC y reclamos en proyectos mineros (Quellaveco, Tía María, Cerro Verde, Pan American Silver).
