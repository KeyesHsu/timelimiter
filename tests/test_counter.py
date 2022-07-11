from unittest import TestCase

from timelimiter.counter import Counter


class TestCounter(TestCase):
    def test_reset(self):
        counter = Counter()
        self.assertEqual(0, counter.val)

        counter.inc()
        self.assertEqual(1, counter.val)
        counter.inc(2)
        self.assertEqual(3, counter.val)

        counter.dec()
        self.assertEqual(2, counter.val)
        counter.dec(1)
        self.assertEqual(1, counter.val)

        counter.reset()
        self.assertEqual(0, counter.val)
