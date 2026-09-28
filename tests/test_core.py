import unittest,sys; sys.path.insert(0,'src')
from agent_scheduler_sim.core import *
class T(unittest.TestCase):
 def test_complete(self): self.assertEqual(simulate([{'id':'a','arrival':0,'duration':1}],1)['completed'],1)
 def test_retry(self): self.assertEqual(simulate([{'id':'a','arrival':0,'duration':1,'fail_attempts':1,'max_retries':1}],1)['attempts']['a'],2)
 def test_priority(self):
  r=simulate([{'id':'a','arrival':0,'duration':5,'priority':0},{'id':'b','arrival':0,'duration':1,'priority':10}],1); self.assertGreater(r['max_queue_latency'],0)
