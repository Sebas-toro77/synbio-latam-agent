from unittest.mock import MagicMock, patch
import pytest
from synbio_agent.schemas import (
    CommunityCollaboration,
    ExperienceItem,
    LearningNeedItem,
    MemberProfilePayload,
)
from synbio_agent.nodes.extraction import extraction_node
from synbio_agent.state import AgentState


@pytest.fixture
def sample_markdown_input() -> str:
    """Fixture que provee un texto Markdown representativo de un usuario."""
    return """
    ### 1. RESUMEN EJECUTIVO
    Biotecnóloga paraguaya cursando máster en Fisiología Vegetal.

    ### 2. EXPERIENCIAS Y PROYECTOS DESTACADOS
    - **Actividad / Proyecto:** Validación de transcritos por qPCR asociados a coloración floral.
      - **Categoría:** wet_lab_experimental
      - **Contexto:** Tesis de Máster
      - **Rol:** ejecutó
      - **Técnicas, Software y Metodologías:** qPCR, Extracción de RNA
      - **Evidencia textual:** "Valida por qPCR transcritos diferencialmente expresados"

    ### 3. NECESIDADES DE APRENDIZAJE (PRÓXIMOS 6 MESES)
    - **Tema prioritario:** Pipelines de transcriptómica
      - **Urgencia:** alta
      - **Motivo / Contexto:** Necesario para su investigación de tesis

    ### 4. COLABORACIÓN Y COMUNIDAD
    - **Puedo enseñar / dar mentoría en:** qPCR, Cultivo in vitro
    - **Apoyo que busca:** Acceso a infraestructura de secuenciación
    - **Espacios de interés:** Mentorías 1 a 1
    """


@pytest.fixture
def mock_profile_payload() -> MemberProfilePayload:
    """Fixture con un objeto MemberProfilePayload válido."""
    return MemberProfilePayload(
        resumen_ejecutivo="Biotecnóloga paraguaya cursando máster en Fisiología Vegetal.",
        experiencias=[
            ExperienceItem(
                actividad="Validación de transcritos por qPCR",
                categoria="wet_lab_experimental",
                contexto="Tesis de Máster",
                rol="ejecutó",
                tecnicas_herramientas=["qPCR", "Extracción de RNA"],
                evidencia_textual="Valida por qPCR transcritos diferencialmente expresados",
            )
        ],
        necesidades_aprendizaje=[
            LearningNeedItem(
                tema_prioritario="Pipelines de transcriptómica",
                urgencia="alta",
                motivo_contexto="Necesario para su investigación de tesis",
            )
        ],
        colaboracion_comunidad=CommunityCollaboration(
            puedo_ensenar=["qPCR", "Cultivo in vitro"],
            apoyo_que_busca="Acceso a infraestructura de secuenciación",
            espacios_de_interes="Mentorías 1 a 1",
        ),
    )


@patch("synbio_agent.nodes.extraction.ChatPromptTemplate")
@patch("synbio_agent.nodes.extraction.ChatOllama")
def test_extraction_node_success(
    mock_chat_ollama: MagicMock,
    mock_prompt_template: MagicMock,
    sample_markdown_input: str,
    mock_profile_payload: MemberProfilePayload,
):
    """Verifica que el nodo procese correctamente el Markdown usando el mock de ChatOllama."""
    # Mock del chain resultante de `prompt | structured_llm`
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = mock_profile_payload

    # Mock del prompt para que `prompt | structured_llm` retorne mock_chain
    mock_prompt = MagicMock()
    mock_prompt.__or__ = MagicMock(return_value=mock_chain)
    mock_prompt_template.from_messages.return_value = mock_prompt

    # Mock del LLM (ChatOllama)
    mock_llm_instance = MagicMock()
    mock_chat_ollama.return_value = mock_llm_instance

    input_state: AgentState = {
        "response_id": "resp-12345",
        "email": "usuario@synbiolatam.org",
        "raw_markdown": sample_markdown_input,
        "parsed_profile": None,
        "extraction_error": None,
        "db_status": None,
    }

    result = extraction_node(input_state)

    assert result["parsed_profile"] is not None
    assert result["extraction_error"] is None
    assert result["parsed_profile"].resumen_ejecutivo == mock_profile_payload.resumen_ejecutivo
    assert len(result["parsed_profile"].experiencias) == 1
    assert result["parsed_profile"].experiencias[0].categoria == "wet_lab_experimental"


def test_extraction_node_empty_input():
    """Verifica el comportamiento cuando el texto de entrada está vacío (no llama al LLM)."""
    input_state: AgentState = {
        "response_id": "resp-99999",
        "email": "vacio@synbiolatam.org",
        "raw_markdown": "   ",
        "parsed_profile": None,
        "extraction_error": None,
        "db_status": None,
    }

    result = extraction_node(input_state)

    assert result["parsed_profile"] is None
    assert result["extraction_error"] == "El contenido raw_markdown está vacío."


@patch("synbio_agent.nodes.extraction.ChatPromptTemplate")
@patch("synbio_agent.nodes.extraction.ChatOllama")
def test_extraction_node_llm_exception(
    mock_chat_ollama: MagicMock,
    mock_prompt_template: MagicMock,
    sample_markdown_input: str,
):
    """Verifica el manejo de errores cuando Ollama no responde o lanza una excepción."""
    # Mock del chain que lanza excepción en invoke
    mock_chain = MagicMock()
    mock_chain.invoke.side_effect = Exception("Ollama connection refused at localhost:11434")

    mock_prompt = MagicMock()
    mock_prompt.__or__ = MagicMock(return_value=mock_chain)
    mock_prompt_template.from_messages.return_value = mock_prompt

    mock_llm_instance = MagicMock()
    mock_chat_ollama.return_value = mock_llm_instance

    input_state: AgentState = {
        "response_id": "resp-error",
        "email": "error@synbiolatam.org",
        "raw_markdown": sample_markdown_input,
        "parsed_profile": None,
        "extraction_error": None,
        "db_status": None,
    }

    result = extraction_node(input_state)

    assert result["parsed_profile"] is None
    assert "Error procesando la extracción Pydantic con Ollama" in result["extraction_error"]
    assert "Ollama connection refused" in result["extraction_error"]