from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# Enumerados estrictos para evitar deriva de etiquetas (Schema Drift)
CategoryType = Literal[
    "wet_lab_experimental",
    "bioprocesos_escalado",
    "dry_lab_bioinformatica_ia",
    "regulacion_bioseguridad_bioetica",
    "propiedad_intelectual_transferencia",
    "gestion_proyectos_emprendimiento",
    "educacion_divulgacion_comunidad",
    "otro"
]

RoleType = Literal["apoyó", "ejecutó", "lideró", "enseñó", "no_claro"]

UrgencyType = Literal["alta", "media", "baja", "no_claro"]


class ExperienceItem(BaseModel):
    actividad: str = Field(
        description="Descripción concisa de la actividad, proyecto o investigación realizada."
    )
    categoria: CategoryType = Field(
        description="Categoría principal según la taxonomía de 7 áreas de SynBio LATAM."
    )
    contexto: Optional[str] = Field(
        default="no_claro",
        description="Institución, empresa, proyecto o duración aproximada de la experiencia."
    )
    rol: RoleType = Field(
        description="Rol observado en la ejecución de la actividad, respaldado por la evidencia."
    )
    tecnicas_herramientas: List[str] = Field(
        default_factory=list,
        description="Lista de software, metodologías, técnicas de laboratorio o marcos aplicados."
    )
    evidencia_textual: str = Field(
        description="Cita textual exacta o frase corta del usuario que sustenta el rol o ejecución."
    )


class LearningNeedItem(BaseModel):
    tema_prioritario: str = Field(
        description="Habilidad, software o concepto técnico prioritario a aprender."
    )
    urgencia: UrgencyType = Field(
        description="Nivel de urgencia declarado o inferido del aprendizaje."
    )
    motivo_contexto: Optional[str] = Field(
        default="no_claro",
        description="Motivo, proyecto de tesis o meta laboral que justifica la necesidad."
    )


class CommunityCollaboration(BaseModel):
    puedo_ensenar: List[str] = Field(
        default_factory=list,
        description="Temas, técnicas o herramientas que domina y ofrece para enseñar o dar mentoría."
    )
    apoyo_que_busca: Optional[str] = Field(
        default=None,
        description="Tipos de apoyo comunitario requeridos (equipos, financiamiento, redes, etc.)."
    )
    espacios_de_interes: Optional[str] = Field(
        default=None,
        description="Formatos preferidos de interacción comunitaria (talleres, 1 a 1, eventos informales)."
    )


class MemberProfilePayload(BaseModel):
    resumen_ejecutivo: str = Field(
        description="Síntesis ejecutiva del perfil profesional, área principal de especialidad y meta."
    )
    experiencias: List[ExperienceItem] = Field(
        description="Listado estructurado de experiencias y proyectos destacados."
    )
    necesidades_aprendizaje: List[LearningNeedItem] = Field(
        description="Temas prioritarios de aprendizaje a 6 meses."
    )
    colaboracion_comunidad: CommunityCollaboration = Field(
        description="Intereses de mentoría, oferta docente y necesidades de red comunitaria."
    )