import csv
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from reproduce import calculate, read

class TestReproduction(unittest.TestCase):
    def test_historical_totals(self):
        s = calculate()
        self.assertEqual(s['stage_counts'], [50, 30, 12, 5, 3])
        self.assertEqual(s['completed_jobs'], 185377)
        self.assertEqual(s['training_participations'], 1450)
        self.assertEqual(s['not_field_tested_pct'], 90)
        self.assertEqual(s['reported_venture_to_problem_pct'], 6)
        self.assertFalse(s['venture_crosswalk_verified'])
        self.assertNotIn('reported_venture_to_field_ratio_pct', s)
    def test_ventures(self):
        self.assertEqual({v['name'] for v in read('startup_pathways.csv')}, {'PakHPC', 'PakASIC', 'FootAnalytic'})
        with (ROOT / 'results' / 'funnel.csv').open(newline='') as f:
            self.assertEqual(list(csv.DictReader(f))[-1]['percent_of_previous_reported_count'], '')
    def test_cutoff(self):
        for name in ('annual_hpc.csv', 'annual_innovation.csv'):
            self.assertEqual([int(r['year']) for r in read(name)], list(range(2019, 2026)))
        self.assertTrue(all(r['reported_publication_date'].startswith('2026') for r in read('post_study_dataset_index.csv')))
    def test_hpc_growth(self):
        s = calculate()
        self.assertEqual(s['change_2024_to_2025_pct'], {'reported_active_users':100.0, 'completed_jobs':97.1321})
        self.assertEqual(s['jobs_per_reported_user_2024'], 64.02)
        self.assertEqual(s['jobs_per_reported_user_2025'], 63.102)
    def test_legacy_accounting_isolation(self):
        s = calculate()
        self.assertNotIn('aggregate_accounting_hours', s)
        h = read('annual_hpc.csv')
        self.assertEqual(sum(int(r['aggregate_accounting_hours']) for r in h), 1248952)
        self.assertNotIn('accounting', (ROOT/'results'/'hpc_yearly_changes.csv').read_text())
        self.assertIn('not physical utilization', (ROOT/'results'/'legacy_accounting_changes.csv').read_text())
    def test_management_context_not_promoted(self):
        self.assertNotIn('financing', calculate())
        self.assertNotIn('interviews', calculate())
        r = read('management_clarifications/financing_2025.csv')
        self.assertEqual([int(x['reported_share_pct']) for x in r], [70, 30])
        self.assertTrue(all(x['reporting_year']=='2025' for x in r))
        f = read('management_clarifications/stakeholder_feedback.csv')
        self.assertEqual([int(x['reported_value']) for x in f], [200, 100])
    def test_blank_templates(self):
        for p in (ROOT/'templates').glob('*.csv'):
            with p.open(newline='') as f:
                self.assertEqual(list(csv.DictReader(f)), [], p.name)

if __name__ == '__main__':
    unittest.main()
