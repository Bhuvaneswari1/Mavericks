"""Offline input and routing regression tests; no secrets or paid calls."""
import unittest,tempfile
from pathlib import Path
from shared.core import ROOT,Knowledge,lookup,records,documents
from shared.graph import route_question
class WorkshopTests(unittest.TestCase):
    def test_known_request(self): self.assertEqual(lookup('SR1001')['status'],'Pending')
    def test_unknown_request(self): self.assertIn('error',lookup('SR9999'))
    def test_policy_retrieval(self): self.assertTrue(Knowledge(ROOT/'data/policies.csv').search('account opening documents'))
    def test_unknown_policy(self): self.assertEqual(Knowledge(ROOT/'data/policies.csv').search('lunar cheese rate'),[])
    def test_routes(self):
        self.assertEqual(route_question('status sr1001'),'request')
        self.assertEqual(route_question('lost card'),'policy')
        self.assertEqual(route_question('hello'),'general')
    def test_bad_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'; p.write_text('wrong\nx\n')
            with self.assertRaises(ValueError): records(p,['request_id'])
    def test_duplicate_policy(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'; p.write_text('policy_id,topic,content\nP1,card,hello\nP1,card,again\n')
            with self.assertRaises(ValueError): documents(p)
if __name__=='__main__': unittest.main()
