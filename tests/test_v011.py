import unittest

from agent_scheduler_sim.core import simulate


class SchedulerUpgradeTests(unittest.TestCase):
    def test_fifo_and_priority_produce_different_deadline_outcome(self):
        rows = [
            {"id": "low", "arrival": 0, "duration": 5, "priority": 0, "deadline": 5},
            {"id": "high", "arrival": 0, "duration": 1, "priority": 10, "deadline": 2},
        ]
        priority = simulate(rows, workers=1, policy="priority")
        fifo = simulate(rows, workers=1, policy="fifo")
        self.assertNotIn("high", priority["deadline_misses"])
        self.assertIn("high", fifo["deadline_misses"])

    def test_retry_delay_is_accounted(self):
        result = simulate([{"id": "x", "arrival": 0, "duration": 1, "fail_attempts": 2, "max_retries": 2, "backoff": 2}], workers=1)
        self.assertEqual(result["attempts"]["x"], 3)
        self.assertEqual(result["retry_delay_total"]["x"], 6)

    def test_invalid_policy_fails_fast(self):
        with self.assertRaises(ValueError):
            simulate([], policy="random")


if __name__ == "__main__":
    unittest.main()
