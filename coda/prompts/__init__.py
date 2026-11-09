from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent


def read_prompt_file(name: str) -> str:
    """Load one prompt file from the CODA prompts directory."""

    return (PROMPTS_DIR / name).read_text(encoding="utf-8")
