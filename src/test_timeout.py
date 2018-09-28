from unittest import TestCase
from sched import scheduler
from src.timeout import ScheduledTimeout, timeout


class TestScheduledTimeout(TestCase):
    def test_timeout_when_not_triggered(self):
        with timeout(1000):
            self.assertEqual(1, 1)

    def test_timeout_when_triggered(self):
        clock = LogicalClock()

        with self.assertRaises(TimeoutError, msg="Timed out"):
            with ScheduledTimeout(1, "Timed out", scheduler(clock.time, lambda: None)):
                self.assertTrue(1 == 2)


class LogicalClock:
    def __init__(self):
        self.now = 0

    def time(self):
        self.now += 1

        return self.now
