import pytest
from pydantic import ValidationError
from synbio_agent.schemas import ExperienceItem

def test_valid_experience_item():
    item = ExperienceItem(
        actividad="Transformación de callos de arroz y qPCR",
        categoria="wet_lab_experimental",
        contexto="Tesis de Máster",
        rol="ejecutó",
        tecnicas_herramientas=["qPCR", "Extracción de RNA"],
        evidencia_textual="Valida por qPCR transcritos diferencialmente expresados"
    )
    assert item.categoria == "wet_lab_experimental"
    assert item.rol == "ejecutó"

def test_invalid_category_raises_error():
    with pytest.raises(ValidationError):
        ExperienceItem(
            actividad="Prueba invalida",
            categoria="categoria_inexistente",  # Debe fallar por no estar en el Literal
            rol="ejecutó",
            evidencia_textual="Prueba"
        )