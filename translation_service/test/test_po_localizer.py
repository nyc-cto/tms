import unittest
import po_localizer

# TODO: Make unittests for other .py files
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
    main

translators.py ???
    CapsTranslator.translate
    GoogleTranslator.__init__?
    GoogleTranslator.translate
    TranslatorFactory.get_translator

"""


class TestPoLocalizer(unittest.TestCase):

    def test_localize_po_file(self):
        """
        localize_po_file
            expected in: in_path, out_path, po_file, target_lang_iso, translator
            expected out: localized po_files written to out_path

        # Call localize_po_file on a file in the in_path
        # check that the file exists in the out_path dir?
        # check anything else?
        # check any edge cases?
        """
        self.assertTrue(True)  # TODO: Fix

    def test_parse_po_lines(self):
        """
    parse_po_lines
        expected in: po_filepath (golden file)
        expected out: po_lines, po_msgstr_texts (golden file?)

        # Call parse_po_lines on a golden file
        # check that the returned two lists match golden ones (in file?)
        # check anything else?
        # check any edge cases?
        """
        self.assertTrue(True)  # TODO: Fix

    def test_write_po_localized_file(self):
        """
        write_po_localized_file
            expected in: localized_po_filepath, po_lines, localized_texts
            expected out: localized .po file which has the localized strs (golden file)

        # Call write_po_localized_file
        # check that the file is written to the correct place
        # check that the file matches golden file (with golden input for po_lines, localized_texts)
        # check anything else?
        # check any edge cases?
        """
        self.assertTrue(True)  # TODO: Fix


if __name__ == '__main__':
    unittest.main()
