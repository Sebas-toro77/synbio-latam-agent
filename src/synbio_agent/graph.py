from langgraph.graph import StateGraph, END
from synbio_agent.state import AgentState
from synbio_agent.nodes.extraction import extraction_node

def should_continue_to_db(state: AgentState) -> str:
    """Ruta condicional: si la extracción falla, redirige a manejo de errores."""
    if state.get("extraction_error"):
        return "error_handler"
    return "taxonomy_normalizer_node"

def error_handler_node(state: AgentState) -> Dict[str, Any]:
    """Nodo para registrar fallos de parsing en la BD o reintento."""
    print(f"[ERROR DE EXTRACCIÓN]: ID {state['response_id']} - {state['extraction_error']}")
    return {"db_status": "FAILED_EXTRACTION"}

# Construcción del Grafo
builder = StateGraph(AgentState)

# Agregar nodos
builder.add_node("extract_profile", extraction_node)
builder.add_node("error_handler", error_handler_node)
# builder.add_node("taxonomy_normalizer_node", taxonomy_normalizer_node)

# Flujo de ejecución
builder.set_entry_point("extract_profile")

builder.add_conditional_edges(
    "extract_profile",
    should_continue_to_db,
    {
        "error_handler": "error_handler",
        "taxonomy_normalizer_node": END # Reemplazar con el siguiente nodo del pipeline
    }
)

app = builder.compile()