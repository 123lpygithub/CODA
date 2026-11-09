"""Create an immutable nine-run sensitivity plan from frozen formal packets."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coda.sensitivity import build_sensitivity_protocol
from coda.study import validate_study_packet
from coda.evaluator import validate_frozen_selection


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, action='append', required=True)
    parser.add_argument('--reference-models', type=Path, required=True, help='JSON mapping every LLM role to a model')
    parser.add_argument('--selection', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20260907)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Refusing to overwrite a frozen protocol.')
    packets = {}
    for path in args.packet:
        packet = json.loads(path.read_text())
        validate_study_packet(packet, 'formal')
        if packet['dataset_name'] in packets: parser.error('Duplicate dataset packet.')
        packets[packet['dataset_name']] = packet
    selection = json.loads(args.selection.read_text())
    for packet in packets.values(): validate_frozen_selection(selection, packet=packet)
    if not selection.get('selection_frozen'): parser.error('Evaluator selection has not been frozen.')
    protocol = build_sensitivity_protocol(packets, seed=args.seed,
        reference_models=json.loads(args.reference_models.read_text()),
        evaluator_models=selection['selected_candidate_models'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(protocol, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'output': str(args.output), 'runs': len(protocol['runs'])}))


if __name__ == '__main__': main()
