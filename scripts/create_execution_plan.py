"""Freeze the six-participant allocation; this creates no runs or model calls."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coda.execution import build_execution_plan
from coda.study import load_study_manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--roster', type=Path, required=True)
    parser.add_argument('--phase', choices=['pilot', 'formal'], required=True)
    parser.add_argument('--exclude-roster', type=Path, help='Other phase roster to enforce separate reviewers')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20260907)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite a frozen allocation.')
    excluded = json.loads(args.exclude_roster.read_text()) if args.exclude_roster else []
    plan = build_execution_plan(load_study_manifest(args.manifest), json.loads(args.roster.read_text()),
        phase=args.phase, seed=args.seed,
        excluded_participant_ids=[person['participant_id'] for person in excluded])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'runs': len(plan['runs'])}))


if __name__ == '__main__':
    main()
