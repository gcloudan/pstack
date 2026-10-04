import unittest
from reminders import Session, reminder, render

class ReminderTests(unittest.TestCase):
    def test_boundary(self):
        self.assertIsNone(reminder(Session(29)))
        self.assertEqual(render(Session(30)), 'stretch after 30 minutes')

    def test_paused(self):
        self.assertIsNone(reminder(Session(90, paused=True)))

    def test_override(self):
        self.assertIsNone(reminder(Session(30), threshold=60))
        self.assertEqual(reminder(Session(60), threshold=60)['minutes'], 60)
