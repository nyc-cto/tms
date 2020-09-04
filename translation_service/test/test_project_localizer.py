import unittest
import sys
sys.path.append('src')
import project_localizer

# TODO: Create tests for these functions
"""
project_localizer.py
    localize_project
        expected in: input_dir, output_dir, translation_api, google_key_path
        expected out: localization subdirs created in output_dir (and localized po_files inside)
    create_output_localized_subdir
        expected in: output_dir, target_lang_iso
        expected out: subdir for target_lang_iso created if not already there in output_dir
    validate_args
        expected_in: input_dir, output_dir, translation_api, google_key_path
        expected_out: Error if any of these is invalid (# TODO: refactor to create ErrorHandler that calls sys.exit)
"""


class TestPoLocalizer(unittest.TestCase):

    def test_todo(self):
        self.assertTrue(False)  # TODO: Fix


if __name__ == '__main__':
    unittest.main()
