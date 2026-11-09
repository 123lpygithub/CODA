"""Export randomly ordered blind scoring packets and an unscored human worksheet.

Keep the private index separate from evaluators. Empty score cells are inputs
for real independent ratings, never experimental measurements.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coda.agents.evaluator_agent import build_blinded_evaluator_packet
from coda.study import scoring_assignment_targets, validate_study_packet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, action='append', required=True)
    parser.add_argument('--phase', choices=['pilot','formal'], required=True)
    parser.add_argument('--evaluator-id', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20260907)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error('Use a new output directory to preserve the frozen presentation.')
    packets = [json.loads(path.read_text()) for path in args.packet]
    if len({packet['run_id'] for packet in packets}) != len(packets):
        parser.error('Duplicate run packet.')
    for packet in packets:
        validate_study_packet(packet,args.phase)
    packets.sort(key=lambda item:item['run_id'])
    random.Random(args.seed).shuffle(packets)
    private_index, worksheet = {}, []
    args.output_dir.mkdir(parents=True)
    for index, packet in enumerate(packets,1):
        label = f'output-{index:03d}'
        targets = scoring_assignment_targets(packet,args.phase)
        packet['scoring_assignment_targets'] = targets
        packet['evaluation_scope'] = 'codebook_and_assignments'
        blinded = build_blinded_evaluator_packet(packet,seed=args.seed)
        (args.output_dir/f'{label}.json').write_text(json.dumps(blinded,ensure_ascii=False,indent=2)+'\n')
        private_index[label] = {'run_id':packet['run_id'], 'dataset_name':packet['dataset_name'],
                                'study_materials':packet['study_materials']}
        base = {'blind_output_id':label,'evaluator_id':args.evaluator_id,'evaluator_kind':'human',
                'phase':args.phase,'status':'assessable','score':None,'rationale':''}
        worksheet.extend({**base,'unit':'codebook','dimension':dimension} for dimension in (
            'clarity','category_boundaries','meaningful_coverage'))
        worksheet.extend({**base,'unit':'assignment','dimension':'evidence_support',
                          'artifact_id':artifact,'code_id':code} for artifact,codes in targets.items() for code in codes)
    (args.output_dir/'worksheet.json').write_text(json.dumps(worksheet,ensure_ascii=False,indent=2)+'\n')
    # Identifiers here permit reintegration after scoring; never share this file
    # alongside blind material with the independent raters.
    (args.output_dir/'private_index.json').write_text(json.dumps({
        'presentation_seed':args.seed,'outputs':private_index},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'outputs':len(packets),'targets':len(worksheet),'output_dir':str(args.output_dir)}))


if __name__ == '__main__':
    main()
