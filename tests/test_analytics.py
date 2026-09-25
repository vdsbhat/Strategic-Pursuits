import importlib.util
import json
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('build',ROOT/'build.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

class AnalyticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data,cls.rows=b.build_data()
    def test_no_footprint_preserved(self): self.assertEqual(b.deployment(['No Footprint']),'No Footprint')
    def test_mixed_deployment(self): self.assertEqual(b.deployment(['Cloud','On-Premise']),'Hybrid')
    def test_explicit_hybrid(self): self.assertEqual(b.deployment(['Hybrid','Cloud']),'Hybrid')
    def test_cloud(self): self.assertEqual(b.deployment(['Cloud']),'Cloud')
    def test_no_footprint_modernization(self): self.assertEqual(b.modernization('No Footprint',100),0)
    def test_modernization_boundary(self): self.assertEqual((b.modernization('On-Premise',59),b.modernization('On-Premise',60)),(55,85))
    def test_classification_precedence(self):
        self.assertEqual(b.classify('No Footprint',0,100),'Whitespace')
        self.assertEqual(b.classify('Hybrid',65,100),'Modernization')
        self.assertEqual(b.classify('Cloud',20,60),'Competitive')
        self.assertEqual(b.classify('Cloud',20,59),'Expansion')
    def test_bands(self):
        for value,expected in [(0,'Not Prioritized'),(39.9,'Not Prioritized'),(40,'Emerging'),(54.9,'Emerging'),(55,'Moderate'),(69.9,'Moderate'),(70,'Strong'),(84.9,'Strong'),(85,'Very Strong'),(100,'Very Strong')]: self.assertEqual(b.band(value),expected)
    def test_weights_sum(self): self.assertEqual(sum(w for _,w in b.COMPONENTS),100)
    def test_score_extremes(self): self.assertEqual((b.score([0]*7),b.score([100]*7)),(0,100))
    def test_rounding_regression(self): self.assertEqual(b.score([69.5,100,55,0,20,0,0]),45.2)
    def test_constant_normalization(self): self.assertEqual(b.minmax([7,7]),[0,0])
    def test_normalization(self): self.assertEqual(b.minmax([0,50,100]),[0,50,100])
    def test_grain(self): self.assertEqual(len({(r['ai'],r['pi']) for r in self.rows}),21000)
    def test_pipeline_reconciles(self):
        source=sum(float(r['amount']) for r in self.data['_tables']['opportunities'] if r['status']=='Open')
        self.assertEqual(sum(r['pipeline'] for r in self.rows),source)
    def test_whitespace_reconciles(self): self.assertEqual(sum(r['deployment']=='No Footprint' for r in self.rows),5948)
    def test_ai_ml_deployment(self): self.assertTrue(all(r['deployment'] in ['Cloud','No Footprint'] for r in self.rows if b.PRODUCTS[r['pi']]=='AI & ML'))
    def test_ranks(self):
        self.assertEqual([r['rank'] for r in self.rows],list(range(1,21001)))
        self.assertTrue(all(self.rows[i]['score']>=self.rows[i+1]['score'] for i in range(len(self.rows)-1)))
    def test_scores_recompute(self): self.assertTrue(all(r['score']==b.score(r['signals']) and r['band']==b.band(r['score']) for r in self.rows))
    def test_snapshot(self):
        self.assertEqual(self.data['audit']['strategic'],8375)
        self.assertEqual(self.data['audit']['bands']['Very Strong'],83)
        self.assertEqual(self.data['audit']['bands']['Strong'],2665)
    def test_scenario_bands(self):
        by_key={(self.data['accounts'][r['ai']]['account_id'],b.PRODUCTS[r['pi']]):r for r in self.rows}
        self.assertEqual(len(self.data['scenarios']),21000)
        for s in self.data['scenarios']:
            self.assertEqual(by_key[s['account_id'],s['product_family']]['pipeline'],s['open_pipeline'])
            self.assertIn(s['product_stage'],['Quiet','Exploring','Evaluating','Advanced evaluation'])
    def test_baseline_preserved(self):
        baseline,rows=b.build_data(enriched=False)
        self.assertEqual((baseline['audit']['strategic'],baseline['audit']['max_score']),(624,72.9))
        modified={s['account_id'] for s in self.data['scenarios']}
        lookup={(r['ai'],r['pi']):r for r in rows}
        for r in self.rows:
            if self.data['accounts'][r['ai']]['account_id'] not in modified:
                self.assertEqual(r['score'],lookup[r['ai'],r['pi']]['score'])
    def test_all_bands_populated(self):
        self.assertTrue(all(self.data['audit']['bands'].get(band,0)>0 for band in b.BANDS))
    def test_demographics_and_footprints_preserved(self):
        baseline,_=b.build_data(enriched=False)
        self.assertEqual(self.data['_tables']['accounts'],baseline['_tables']['accounts'])
        self.assertEqual(self.data['_tables']['product_footprint'],baseline['_tables']['product_footprint'])
    def test_reproducible(self):
        again,rows=b.build_data()
        self.assertEqual(self.rows,rows)
        self.assertEqual(self.data['scenarios'],again['scenarios'])
    def test_standalone(self):
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        self.assertNotIn('<script src=',html);self.assertNotIn('<link rel="stylesheet"',html)
        for marker in ['/*__DATA__*/','/*__APP__*/','/*__CORE__*/','/*__STYLE__*/']: self.assertNotIn(marker,html)

if __name__=='__main__': unittest.main(verbosity=2)
