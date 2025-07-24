from django.test import SimpleTestCase


class Smoke(SimpleTestCase):
    """Minimal sanity check to prove test discovery works."""
    def test_truth(self):
        self.assertTrue(True)
