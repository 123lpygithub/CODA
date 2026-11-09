"""Run one independent LLM evaluator over a frozen RQ1 packet."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from coda.agents.evaluator_agent import EvaluatorLLMAgent
from coda.llm import LLMModelConfig, load_chat_backend
from coda.study import StudyManifestError, validate_study_packet, scoring_assignment_targets
from coda.evaluator import validate_frozen_selection


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="Frozen rq1_materials.json packet")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--evaluator-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--phase", choices=("pilot", "formal"), default="formal")
    parser.add_argument("--candidate-model")
    parser.add_argument("--selection", type=Path, help="Frozen three-model calibration result (required for formal LLM scoring).")
    parser.add_argument(
        "--artifact-chunk-size",
        type=int,
        default=8,
        help="Number of artifacts per evaluator call for large frozen packets.",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--exploratory", action="store_true",
        help="Score an unbound diagnostic packet; output is not study-verified.",
    )
    args = parser.parse_args()

    if args.candidate_model is not None and args.candidate_model != args.model:
        parser.error("--candidate-model must match the actual --model; evaluator identities cannot be relabeled.")

    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    if not isinstance(packet, dict):
        parser.error("The packet must be a JSON object.")
    if args.artifact_chunk_size < 1:
        parser.error("--artifact-chunk-size must be positive.")
    binding = None
    if packet.get("run_id") != args.run_id:
        parser.error("--run-id must match the packet's run_id.")
    if packet.get("study_materials") is not None or not args.exploratory:
        try:
            binding = validate_study_packet(packet, args.phase)
        except StudyManifestError as error:
            parser.error(str(error))
    if args.phase == "formal" and not args.exploratory:
        if args.selection is None:
            parser.error("Formal scoring requires --selection with the frozen evaluator models.")
        selection = json.loads(args.selection.read_text(encoding="utf-8"))
        validate_frozen_selection(selection, packet=packet)
        selected = selection.get("selected_candidate_models", [])
        if not selection.get("selection_frozen") or len(set(selected)) != 3 or args.model not in selected:
            parser.error("Requested model is outside the frozen three-evaluator selection.")
        sensitivity = packet.get("sensitivity_protocol")
        if sensitivity and set(sensitivity['evaluator_models']) != set(selected):
            parser.error("Evaluator selection differs from the frozen sensitivity protocol.")
    targets = scoring_assignment_targets(packet, args.phase)
    config = LLMModelConfig.from_env(
        default_provider="rightapi",
        default_model=args.model,
        default_max_output_tokens=6000,
        default_retry_timeouts_forever=True,
    )
    if config.model != args.model:
        parser.error("Environment model override differs from the requested evaluator model.")
    agent = EvaluatorLLMAgent(
        model_config=config,
        backend=load_chat_backend(config),
    )
    # Resume the same independently scored targets without asking again merely
    # to obtain another rating. Keep failed/refused physical calls for costing.
    from coda.persistence import append_jsonl
    agent.trace_sink = lambda trace: append_jsonl(args.output.with_suffix('.calls.jsonl'), trace)
    checkpoint_path = args.output.with_suffix('.checkpoint.json')
    signature = hashlib.sha256(json.dumps({
        'packet': packet, 'phase': args.phase, 'evaluator_id': args.evaluator_id,
        'candidate_model': args.candidate_model or args.model,
        'model': asdict(config), 'chunk_size': args.artifact_chunk_size,
        'system_prompt': agent._prompt_spec.system_prompt,
        'user_prompt': agent._prompt_spec.user_prompt_template,
    }, sort_keys=True).encode()).hexdigest()
    checkpoint = json.loads(checkpoint_path.read_text()) if checkpoint_path.exists() else {'signature':signature, 'completed':{}}
    if checkpoint['signature'] != signature:
        parser.error('Evaluator checkpoint differs from these frozen inputs/settings. Use a different output path.')
    def score_once(key, target):
        if key not in checkpoint['completed']:
            checkpoint['completed'][key] = agent(packet=target, run_id=args.run_id,
                evaluator_id=args.evaluator_id, phase=args.phase,
                candidate_model=args.candidate_model or args.model)
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = checkpoint_path.with_suffix('.tmp')
            temporary.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2)+'\n')
            temporary.replace(checkpoint_path)
        return checkpoint['completed'][key]
    artifacts = packet.get("artifacts", [])
    if not isinstance(artifacts, list):
        parser.error("The packet's artifacts field must be a list.")
    artifacts = sorted(artifacts, key=lambda item: str(item['artifact_id']))
    random.Random(20260907).shuffle(artifacts)
    chunks = (
        [artifacts[index : index + args.artifact_chunk_size]
         for index in range(0, len(artifacts), args.artifact_chunk_size)]
        if artifacts
        else [[]]
    )
    # Evaluators need the frozen codebook and artifact-level records, not the
    # full execution trace. Removing trace/history fields keeps every call
    # inside the same documented rubric and avoids accidental prompt bloat.
    packet_base = {
        key: packet[key]
        for key in (
            "run_id",
            "dataset_name",
            "research_question",
            "analysis_protocol",
            "codebook",
            "evaluation_notes",
        )
        if key in packet
    }
    rows: list[dict[str, object]] = []
    # Codebook coverage requires the complete inspected corpus. Do not score
    # it from only the first assignment chunk or average local coverage scores.
    codebook_packet = deepcopy(packet_base)
    codebook_packet["artifacts"] = artifacts
    codebook_packet["evaluation_scope"] = "codebook_only"
    rows.extend(score_once('codebook', codebook_packet))
    for index, chunk in enumerate(chunks):
        if not any((item.get("coding_record") or {}).get("final_code_ids") for item in chunk):
            continue
        chunk_packet = deepcopy(packet_base)
        chunk_packet["artifacts"] = chunk
        chunk_packet["evaluation_scope"] = "assignments_only"
        chunk_packet["scoring_assignment_targets"] = {
            str(item["artifact_id"]): targets.get(str(item["artifact_id"]), []) for item in chunk
        }
        rows.extend(score_once(f'assignments-{index}', chunk_packet))
    unique: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = (
            row.get("dimension"),
            row.get("unit"),
            row.get("artifact_id"),
            row.get("code_id"),
        )
        unique[key] = row
    rows = list(unique.values())
    for row in rows:
        row["scoring_target_protocol"] = "one_uniform_assignment_per_case" if args.phase == "pilot" else "all_assignments"
        row["sampling_seed"] = 20260907 if args.phase == "pilot" else None
        row["study_materials_verified"] = binding is not None
        row["study_materials"] = binding
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "score_count": len(rows)}))


if __name__ == "__main__":
    main()
