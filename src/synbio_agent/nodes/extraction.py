from typing import Any, Dict, cast
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from synbio_agent.config import settings
from synbio_agent.schemas import MemberProfilePayload
from synbio_agent.state import AgentState


def extraction_node(state: AgentState) -> Dict[str, Any]:
    """Nodo de LangGraph que procesa el texto Markdown enviado por el usuario

    y lo convierte de forma determinista al objeto Pydantic MemberProfilePayload
    utilizando Ollama en local.
    """
    raw_markdown = state.get("raw_markdown", "")

    if not raw_markdown.strip():
        return {
            "parsed_profile": None,
            "extraction_error": "El contenido raw_markdown está vacío.",
        }

    # Inicialización del LLM local vía Ollama
    llm = ChatOllama(
        model=settings.OLLAMA_MODEL,  # Ej: "gemma3:4b", "qwen2.5:7b" o "llama3.2:3b"
        base_url=settings.OLLAMA_BASE_URL,  # Default: "http://localhost:11434"
        temperature=0.0,
    )

    # Inferencia de salida estructurada Pydantic
    structured_llm = llm.with_structured_output(MemberProfilePayload)

    system_prompt = (
        "Eres un agente extractor de datos de alta precisión para SynBio LATAM.\n"
        "Tu tarea es analizar la 'Ficha de Perfil Profesional en Markdown' enviada por un miembro "
        "y mapear cada sección de forma exacta al esquema estructurado JSON/Pydantic suministrado.\n\n"
        "REGLAS OBLIGATORIAS:\n"
        "1. Clasifica cada experiencia en una de las 7 categorías permitidas. Si no encaja claro, usa 'otro'.\n"
        "2. Respeta estrictamente las opciones del enum para los roles ('apoyó', 'ejecutó', 'lideró', 'enseñó', 'no_claro').\n"
        "3. Si un campo opcional no está presente en la Ficha, asigna 'no_claro' o lista vacía según corresponda.\n"
        "4. Extrae la evidencia textual exacta del relato para justificar el rol."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "FICHA EN MARKDOWN A PROCESAR:\n\n{raw_markdown}"),
    ])

    chain = prompt | structured_llm

    try:
        extracted_data = cast(MemberProfilePayload, chain.invoke({
            "raw_markdown": raw_markdown
        }))
        return {"parsed_profile": extracted_data, "extraction_error": None}
    except Exception as e:
        return {
            "parsed_profile": None,
            "extraction_error": f"Error procesando la extracción Pydantic con Ollama: {str(e)}",
        }