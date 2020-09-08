import tempfile
import unittest
import sys
import os
sys.path.append('src')
import po_localizer


GOLDEN_IN_PO_LINES = ['msgid ""',
                      'msgstr ""',
                      '"Content-Type: text/plain; charset=UTF-8\\n"',
                      '"Content-Transfer-Encoding: 8bit\\n"',
                      '"Language: de\\n"',
                      '"Generated-By: Serge 1.4\\n"',
                      '#. /about',
                      '#: File: sample.json',
                      '#: ID: a5eea87543a1a8fad51039d72f407011',
                      'msgid "Let\'s get things translated!"',
                      'msgstr ""',
                      '',
                      'msgid "We can use machine translation to get many localizations "',
                      '"done automatically and quickly."',
                      'msgstr ""',
                      '']

GOLDEN_PO_MSGSTR_TEXTS = ["Let's get things translated!",
                          "We can use machine translation to get many localizations done automatically and quickly."]

GOLDEN_LOCALIZED_TEXTS = ["LET'S GET THINGS TRANSLATED!,"
                          "WE CAN USE MACHINE TRANSLATION TO GET MANY LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."]

GOLDEN_OUT_PO_LINES = ['msgid ""',
                       'msgstr ""',
                       '"Content-Type: text/plain; charset=UTF-8\\n"',
                       '"Content-Transfer-Encoding: 8bit\\n"',
                       '"Language: de\\n"',
                       '"Generated-By: Serge 1.4\\n"',
                       '#. /about',
                       '#: File: sample.json',
                       '#: ID: a5eea87543a1a8fad51039d72f407011',
                       'msgid "Let\'s get things translated!"',
                       'msgstr "LET\'S GET THINGS TRANSLATED!"',
                       '',
                       'msgid "We can use machine translation to get many localizations "',
                       '"done automatically and quickly."',
                       'msgstr ""',
                       '"WE CAN USE MACHINE TRANSLATION TO GET MANY LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."'
                       '']


class TestPoLocalizer(unittest.TestCase):

    def test_localize_po_file(self):
        """
        localize_po_file
            expected in: in_path, out_path, po_file, target_lang_iso, translator
            expected out: localized po_file written to out_path

        # Call localize_po_file on a file in the in_path
        # check that the file exists in the out_path dir?
        # check anything else?
        # check any edge cases?
        """
        # TODO:  test that directory structure formation is as I expect
        #   and also checksum of golden_in and golden_out files

        self.assertTrue(False)  # TODO: Fix

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
        self.assertTrue(False)  # TODO: Fix

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
        self.assertTrue(False)  # TODO: Fix


if __name__ == '__main__':
    unittest.main()
