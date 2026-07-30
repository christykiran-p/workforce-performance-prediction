from pathlib import Path

# ======================================================
# Project Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_analytics_dataset.parquet"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "best_model.pkl"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "prediction_output.csv"
)

KNOWLEDGE_BASE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
)

# ======================================================
# Ollama
# ======================================================

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "phi3:latest"

EMBEDDING_MODEL = "nomic-embed-text"

# ======================================================
# AI
# ======================================================

TEMPERATURE = 0.2
MAX_SUMMARY_TOKENS = 300