#!/usr/bin/env python3
"""Check recorded model outputs; never treat schema validation as behavior evaluation."""
import argparse
import json
import re
from pathlib import Path


def evaluate(assertion, output):
    kind = assertion['check']
    patterns = assertion.get('patterns', [assertion.get('pattern', '')])
    hits = [bool(re.search(p, output)) for p in patterns]
    if kind == 'regex_all':
        return all(hits)
    if kind == 'regex_any':
        return any(hits)
    if kind in ('regex_none', 'regex_none_all'):
        return not any(hits)
    if kind == 'distinct_min':
        return len(set(re.findall(assertion['pattern'], output))) >= assertion['min']
    raise ValueError(f'Unsupported assertion: {kind}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evals', type=Path, default=Path('evals/evals.json'))
    parser.add_argument('--responses', type=Path, required=True,
                        help='JSON: model, revision, outputs [{name, output}]')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    cases = json.loads(args.evals.read_text())['evals']
    data = json.loads(args.responses.read_text())
    for key in ('model', 'revision'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            parser.error(f'Missing provenance: {key}')
    outputs = {}
    for item in data['outputs']:
        name, output = item['name'], item['output']
        if name in outputs or not isinstance(output, str) or not output.strip():
            parser.error(f'Duplicate or empty output: {name}')
        outputs[name] = output
    known = {c['name'] for c in cases}
    if outputs.keys() - known:
        parser.error('Unknown evaluation names')
    results = []
    for case in cases:
        output = outputs.get(case['name'])
        checks = [{ 'id': a['id'], 'passed': evaluate(a, output)}
                  for a in case['assertions']] if output is not None else []
        results.append({'name': case['name'], 'status': 'missing' if output is None
                        else ('passed' if all(x['passed'] for x in checks) else 'failed'),
                        'checks': checks})
    report = {'model': data['model'], 'revision': data['revision'],
              'results': results, 'passed': all(x['status'] == 'passed' for x in results)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
