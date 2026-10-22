
# SynBio LATAM — AI Skill Mapping Agent

[![CI Pipeline](https://github.com/synbiolatam/synbio-latam-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/synbiolatam/synbio-latam-agent/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Agente de Inteligencia Artificial desarrollado en **LangGraph** para la ingesta, extracción estructurada, normalización y almacenamiento relacional del mapa de talento, fortalezas y necesidades de la comunidad **SynBio LATAM**.

El objetivo del sistema es automatizar el procesamiento de fichas profesionales en lenguaje natural (Markdown) recolectadas mediante el formulario comunitario, para estructurarlas en una base de datos relacional (PostgreSQL/Supabase) lista para análisis de brechas y visualización en **Power BI** o **Tableau**.

---

## 🛠️ Arquitectura del Sistema

```text
[Google Forms] ➔ (Markdown Response)
                       │
                       ▼
            [LangGraph Agent Pipeline]
                       │
   ┌───────────────────┴───────────────────┐
   ▼                                       ▼
[Extraction Node]                   [Validation & QA]
(Pydantic Schema parsing)           (Confidence & Evidence verification)
   │                                       │
   └───────────────────┬───────────────────┘
                       │
                       ▼
          [Taxonomy Normalizer Node]
          (Mapping against dim_skill)
                       │
                       ▼
            [PostgreSQL / Supabase]
                       │
                       ▼
         [SQL Views for Power BI / Tableau]

```

---

## 📂 Estructura del Repositorio

```text
synbio-latam-agent/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de Integración Continua (Linter + Tests)
├── data/
│   └── samples/                 # Fichas Markdown de muestra para testing
├── src/
│   └── synbio_agent/
│       ├── __init__.py
│       ├── config.py            # Gestión de variables de entorno y API keys
│       ├── schemas.py           # Modelos Pydantic v2 (MemberProfilePayload, etc.)
│       ├── state.py             # Estado global del grafo (AgentState)
│       ├── graph.py             # Ensamblaje del StateGraph de LangGraph
│       ├── db/                  # Modelos SQLAlchemy y cliente de conexión SQL
│       │   ├── __init__.py
│       │   ├── client.py
│       │   └── models.py
│       └── nodes/               # Nodos modulares del agente
│           ├── __init__.py
│           ├── extraction.py    # Extracción estructurada desde Markdown
│           ├── normalizer.py    # Normalización semántica contra el catálogo
│           └── db_writer.py     # Operaciones de UPSERT en PostgreSQL
├── tests/
│   ├── conftest.py              # Fixtures y mocks para pytest
│   ├── test_schemas.py          # Pruebas de validación de esquemas Pydantic
│   ├── test_extraction.py       # Pruebas unitarias del nodo extractor
│   └── test_graph.py            # Pruebas de integración del flujo en LangGraph
├── pyproject.toml               # Configuración de dependencias (Poetry), Ruff y Pytest
├── README.md
└── poetry.lock

```

---

## 📊 Taxonomía de Clasificación

El agente clasifica automáticamente las experiencias en **7 categorías técnicas estandarizadas**:

1. `wet_lab_experimental`: Biología molecular, microbiología, cultivo in vitro, edición génica.
2. `bioprocesos_escalado`: Fermentación, biorreactores, biomanufactura, purificación.
3. `dry_lab_bioinformatica_ia`: Genómica, bioinformática, R/Python, modelado, IA/ML.
4. `regulacion_bioseguridad_bioetica`: Riesgo biológico, normativas OGM, gobernanza, ELSI.
5. `propiedad_intelectual_transferencia`: Patentes, licenciamiento, transferencia tecnológica.
6. `gestion_proyectos_emprendimiento`: Formulación de grants, startups, desarrollo de negocio, liderazgo.
7. `educacion_divulgacion_comunidad`: Docencia, mentoría, comunicación científica, gestión de redes.

Asimismo, cada experiencia deduce de la evidencia cualitativa un rol observable (`apoyó`, `ejecutó`, `lideró`, `enseñó`, `no_claro`).

---

## 🚀 Requisitos Previos e Instalación

### Requisitos

* **Python:** 3.11 o superior.
* **Poetry:** Gestor de dependencias de Python ([Instrucciones de instalación](https://www.google.com/search?q=https://python-poetry.org/docs/%23installation)).
* **API Key:** Cuenta en OpenAI (o Anthropic/Google Gemini según el proveedor configurado).

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone [https://github.com/synbiolatam/synbio-latam-agent.git](https://github.com/synbiolatam/synbio-latam-agent.git)
cd synbio-latam-agent

```


2. **Instalar dependencias con Poetry:**
```bash
poetry install

```


3. **Configurar variables de entorno:**
Crea un archivo `.env` en la raíz del proyecto basándote en la plantilla:
```bash
cp .env.example .env

```


Añade tu clave de API:
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/synbiolatam_db

```



---

## 🧪 Pruebas y Control de Calidad

Este proyecto utiliza **`pytest`** para pruebas automatizadas (con mocks para evitar llamadas innecesarias a APIs pagadas durante desarrollo) y **`ruff`** para formateo y linting estático.

* **Ejecutar la suite de pruebas:**
```bash
poetry run pytest

```


* **Ejecutar el linter (Ruff):**
```bash
poetry run ruff check .

```


* **Corregir automáticamente advertencias de código:**
```bash
poetry run ruff check --fix .

```



---

## ⚙️ Integración Continua (CI)

El repositorio cuenta con un workflow de **GitHub Actions** (`.github/workflows/ci.yml`) que ejecuta automáticamente en cada `push` o `pull request` hacia `main` o `develop`:

* Instalación limpia de dependencias mediante caché de Poetry.
* Verificación estática de código con `ruff`.
* Ejecución completa de la suite de pruebas unitarias e integración con `pytest`.

---

## 🛡️ Gobernanza y Privacidad de Datos

* **Tratamiento de Datos:** Los nombres y correos electrónicos de los miembros se almacenan en tablas con acceso restringido.
* **Evidencia Cualitativa:** Las respuestas no deben incluir datos personales sensibles ni información confidencial.
* **Trazabilidad:** Toda extracción almacena el texto crudo original en la tabla `respuesta_cruda` junto con su hash y versión del prompt para garantizar auditorías reproducibles.

---

