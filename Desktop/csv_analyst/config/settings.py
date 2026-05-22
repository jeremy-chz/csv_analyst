# config/settings.py
# Paramètres centralisés de l'application

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Chemins ────────────────────────────────────────────────────────────────
ROOT_DIR    = Path(__file__).parent.parent
DATA_RAW    = ROOT_DIR / "data" / "raw"
DATA_SAMPLES = ROOT_DIR / "data" / "samples"

# ── Claude API ────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL             = "claude-sonnet-4-6"
MAX_TOKENS        = 1024

# ── Limites de sécurité ───────────────────────────────────────────────────
MAX_ROWS_PROFILING = 100_000   # au-delà, on échantillonne
MAX_CONTEXT_ROWS   = 5         # nb de lignes exemples envoyées à Claude