from pathlib import Path

import yaml
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent


def load_config() -> dict:
    """Load configs, env and prompts. Return dict"""
    # Key stays in os.environ, never in config
    load_dotenv(BACKEND_DIR / ".env")

    with open(BACKEND_DIR / "config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["system_prompt"] = (BACKEND_DIR / "prompts" / "system.md").read_text(encoding="utf-8")
    config["no_source"] = (BACKEND_DIR / "prompts" / "no_source.md").read_text(encoding="utf-8")
    return config
