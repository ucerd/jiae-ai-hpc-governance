"""Reproduce reported historical aggregate arithmetic, not individual case trajectories."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    with (ROOT / 'data' / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write(name, fields, rows):
    with (ROOT / 'results' / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(fields)
        w.writerows(rows)

def change(old, new):
    return round(100 * (new / old - 1), 4)

def calculate():
    a, h, v = (read(n) for n in ('annual_innovation.csv', 'annual_hpc.csv', 'startup_pathways.csv'))
    def total(rows, key):
        return sum(int(row[key]) for row in rows)
    stage = [total(a, k) for k in ('problem_cases', 'dataset_enabled', 'lab_tested', 'field_tested')] + [len(v)]
    growth = {k: change(int(h[-2][k]), int(h[-1][k])) for k in ('reported_active_users', 'completed_jobs')}
    return dict(study_period='2019–2025', stage_counts=stage,
                stage_counts_note='Reported aggregate counts; stage nesting and case linkage not independently verified. Last count is named emerging venture pathways.',
                training_participations=total(a, 'training_participations'), completed_jobs=total(h, 'completed_jobs'),
                not_field_tested_pct=round(100 * (1 - stage[3] / stage[0]), 4),
                not_field_tested_note='Aggregate complement conditional on nested stages; not permanent abandonment.',
                reported_venture_to_problem_pct=round(100 * stage[4] / stage[0], 4),
                venture_comparison_note='Descriptive count comparison only; no field-to-venture conversion.',
                venture_crosswalk_verified=False, change_2024_to_2025_pct=growth,
                jobs_per_reported_user_2024=round(int(h[-2]['completed_jobs']) / int(h[-2]['reported_active_users']), 4),
                jobs_per_reported_user_2025=round(int(h[-1]['completed_jobs']) / int(h[-1]['reported_active_users']), 4))

def main():
    (ROOT / 'results').mkdir(exist_ok=True)
    s = calculate()
    stages = s['stage_counts']
    names = ['Problem cases', 'Dataset-enabled', 'Lab-tested', 'Field-tested', 'Emerging venture pathways']
    (ROOT / 'results' / 'summary.json').write_text(json.dumps(s, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    write('funnel.csv', ['stage', 'count', 'percent_of_previous_reported_count', 'percent_of_problem_cases', 'interpretation'],
          [(n, c, '' if i in (0, 4) else round(100*c/stages[i-1], 4), round(100*c/stages[0], 4),
            'Named pathways; descriptive comparison only' if i == 4 else 'Aggregate comparison; nested-stage assumption' if i else 'Reported aggregate')
           for i, (n, c) in enumerate(zip(names, stages))])
    h = read('annual_hpc.csv')
    keys = ['reported_active_users', 'completed_jobs']
    write('hpc_yearly_changes.csv', ['year', 'infrastructure_units', 'reported_active_users', 'completed_jobs', 'jobs_per_reported_user'] + [k+'_change_pct' for k in keys],
          [(row['year'], row['infrastructure_units'], row['reported_active_users'], row['completed_jobs'], round(int(row['completed_jobs'])/int(row['reported_active_users']), 4),
            *[change(int(h[i-1][k]), int(row[k])) if i else '' for k in keys]) for i, row in enumerate(h)])
    k = 'aggregate_accounting_hours'
    write('legacy_accounting_changes.csv', ['year', 'legacy_mixed_accounting_entries', 'change_pct_in_legacy_entries', 'interpretation'],
          [(row['year'], row[k], change(int(h[i-1][k]), int(row[k])) if i else '', 'Heterogeneous CPU/GPU administrative entries; not physical utilization or workload intensity') for i, row in enumerate(h)])
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="950" height="390" viewBox="0 0 950 390"><rect width="950" height="390" fill="white"/><g font-family="Arial,sans-serif" fill="#17324d"><text x="24" y="30" font-size="22" font-weight="bold">Reported aggregate stage counts, 2019–2025</text>']
    for i, (n, c) in enumerate(zip(names, stages)):
        y = 62 + i*53
        fill = '#777777' if i == 4 else '#327c8b'
        svg.append(f'<text x="24" y="{y+20}" font-size="17">{n}</text><rect x="290" y="{y}" width="{c*10}" height="28" rx="3" fill="{fill}"/><text x="{300+c*10}" y="{y+20}" font-size="17">{c}</text>')
    svg.append('<text x="24" y="355" font-size="14">Case linkage unverified; venture pathways are a separate reported count, not a conversion.</text></g></svg>')
    (ROOT / 'results' / 'funnel.svg').write_text(''.join(svg), encoding='utf-8')

if __name__ == '__main__':
    main()
