"""Join completed human ratings to private run identifiers and validate every target."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coda.evaluation import validate_rq1_score
from coda.study import verify_study_scores


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('worksheet', type=Path)
    parser.add_argument('--private-index', type=Path, required=True)
    parser.add_argument('--packet', type=Path, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite independent ratings.')
    index = json.loads(args.private_index.read_text())['outputs']
    packets = {}
    for path in args.packet:
        packet = json.loads(path.read_text())
        if packet['run_id'] in packets:
            parser.error('Duplicate packet run ID.')
        packets[packet['run_id']] = packet
    rows = json.loads(args.worksheet.read_text())
    phases = set()
    for row in rows:
        identity = index[row.pop('blind_output_id')]
        row.update(run_id=identity['run_id'], study_materials=identity['study_materials'])
        if row.get('evaluator_kind') != 'human' or not str(row.get('rationale','')).strip():
            parser.error('Every human judgment requires its independent identity and rationale.')
        validate_rq1_score(row)
        phases.add(row['phase'])
    if len(phases) != 1:
        parser.error('Import one scoring phase at a time.')
    verify_study_scores(rows, packets, phases.pop())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ratings':len(rows),'output':str(args.output)}))


if __name__ == '__main__':
    main()
