import unittest
import po_localizer


class TestPoLocalizer(unittest.TestCase):

    def test_translate_to_caps(self):
        self.assertEqual("TEST", po_localizer.translate_to_caps("test"))

    # TODO: Add in more tests


if __name__ == '__main__':
    unittest.main()
