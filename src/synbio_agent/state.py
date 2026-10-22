from typing import TypedDict, Optional
from synbio_agent.schemas import MemberProfilePayload

class AgentState(TypedDict):
    # Inputs recibidos desde el webhook de Google Forms
    response_id: str
    email: str
    raw_markdown: str
    
    # Salidas del nodo de extracción
    parsed_profile: Optional[MemberProfilePayload]
    extraction_error: Optional[str]
    
    # Campos para el nodo de base de datos
    db_status: Optional[str]