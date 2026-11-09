"""Output and result saving for CLIMB."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def save_results(
    output_dir: Path,
    entry_assignments: List[Dict],
    metadata: Dict[str, Any],
) -> Path:
    """Save results to JSON file in evaluation-compatible format."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    results_json = {
        "metadata": metadata,
        "results": entry_assignments,
    }
    results_filename = f"results_{timestamp}.json"
    results_path = output_dir / results_filename
    with open(results_path, "w") as f:
        json.dump(results_json, f, indent=2)
    return results_path
