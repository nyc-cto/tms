import tempfile
import unittest
import sys
import os
import shutil
import hashlib
sys.path.append('src')
import po_file
from translators import TranslatorFactory


GOLDEN_IN_PO_LINES = ['msgid ""\n',
                      'msgstr ""\n',
                      '"Content-Type: text/plain; charset=UTF-8\\n"\n',
                      '"Content-Transfer-Encoding: 8bit\\n"\n',
                      '"Language: de\\n"\n',
                      '"Generated-By: Serge 1.4\\n"\n',
                      '#. /about\n',
                      '#: File: sample.json\n',
                      '#: ID: a5eea87543a1a8fad51039d72f407011\n',
                      'msgid "Let\'s get things translated!"\n',
                      'msgstr ""\n',
                      '\n',
                      'msgid "We can use machine translation to get many localizations "\n',
                      '"done automatically and quickly."\n',
                      'msgstr ""\n']

GOLDEN_PO_MSGSTR_TEXTS = ["", "Let's get things translated!",
                          "We can use machine translation to get many localizations done automatically and quickly."]

GOLDEN_LOCALIZED_TEXTS = ["", "LET'S GET THINGS TRANSLATED!",
                          "WE CAN USE MACHINE TRANSLATION TO GET MANY LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."]

EXAMPLE_FILE = 'example.po'
GOLDEN_EXAMPLE_IN = 'golden_in.po'
GOLDEN_EXAMPLE_OUT = 'golden_out.po'
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
TARGET_LANGUAGE_ISO = 'es'


# TODO: Rewrite the po_localizer tests as po_file tests
class TestPoFile(unittest.TestCase):

    def test_TODO(self):
        self.assertTrue(True)

# class TestPoLocalizer(unittest.TestCase):
#     # Temporary directories & files to read/write during testing
#     temp_root_dir = None
#     temp_in_dir = None
#     temp_out_dir = None
#     in_example_filepath = None
#
#     @classmethod
#     def setUpClass(cls):
#
#         # Make a temporary root directory and inbox/outbox subdirectories to hold the test resources in
#         cls.temp_root_dir = tempfile.mkdtemp()
#         cls.temp_in_dir = os.path.join(cls.temp_root_dir, 'in')
#         cls.temp_out_dir = os.path.join(cls.temp_root_dir, 'out')
#
#         if not os.path.exists(cls.temp_in_dir):
#             os.makedirs(cls.temp_in_dir)
#
#         if not os.path.exists(cls.temp_out_dir):
#             os.makedirs(cls.temp_out_dir)
#
#         # Copy the golden file into the temporary directory inbox
#         golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)
#         cls.in_example_filepath = os.path.join(cls.temp_in_dir, EXAMPLE_FILE)
#         shutil.copyfile(golden_in_filepath, cls.in_example_filepath)
#
#     @classmethod
#     def tearDownClass(cls):
#         # Remove temporary root directory and its subdirectories & files
#         shutil.rmtree(cls.temp_root_dir)
#
#     def test_localize_po_file(self):
#         """
#         localize_po_file
#             expected in: in_path, out_path, po_file (golden), target_lang_iso, translator
#             expected out: localized po_file written to out_path
#         """
#
#         # Create a translator object that does capitalization
#         translator = TranslatorFactory.get_translator(translation_api='caps')
#
#         # Call po_localizer
#         po_localizer.localize_po_file(self.temp_in_dir, self.temp_out_dir, EXAMPLE_FILE,
#                                       TARGET_LANGUAGE_ISO, translator)
#
#         # Get path for where the out file is expected to be written
#         out_example_filepath = os.path.join(self.temp_out_dir, EXAMPLE_FILE)
#
#         # TEST: Ensure the cycle is completed and a file is written in the correct location
#         self.assertTrue(os.path.exists(out_example_filepath))
#
#     def test_parse_po_lines(self):
#         """
#         parse_po_lines
#             expected in: po_filepath (golden)
#             expected out: po_lines, po_msgstr_texts
#         """
#
#         # Call parse_po_lines on a golden example file
#         po_lines, po_msgstr_texts = po_localizer.parse_po_lines(self.in_example_filepath)
#
#         # TEST: Compare the returned arrays to golden versions of the arrays
#         self.assertEqual(po_lines, GOLDEN_IN_PO_LINES)
#         self.assertEqual(po_msgstr_texts, GOLDEN_PO_MSGSTR_TEXTS)
#
#     def test_write_po_localized_file(self):
#         """
#         write_po_localized_file
#             expected in: localized_po_filepath, po_lines (golden), localized_texts (golden)
#             expected out: localized .po file which has the localized texts inserted for the msgstrs
#         """
#
#         # Get path for golden_out comparison file
#         golden_out_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_OUT)
#
#         # Get path for where to write out file
#         out_example_filepath = os.path.join(self.temp_out_dir, EXAMPLE_FILE)
#
#         # Call write_po_localized_file with golden input to write to the out_example_filepath
#         po_localizer.write_po_localized_file(out_example_filepath, GOLDEN_IN_PO_LINES, GOLDEN_LOCALIZED_TEXTS)
#
#         # TEST: Use checksum to ensure the file written out matches the golden file
#         self.assertTrue(compare_files(out_example_filepath, golden_out_filepath))


def get_checksum(filepath):
    """Creates an MD5 checksum for a file.

        Args:
            filepath: The path for the file to create a checksum for.

        Returns:
            The MD5 checksum for the file.
    """

    # Use MD5 to build a checksum for this file
    file_hash = hashlib.md5()

    # Create a checksum of the content of the file
    with open(filepath, 'rb') as f:
        content = f.read()
    file_hash.update(content)

    # Return the checksum for the file
    return file_hash.hexdigest()


def compare_files(file1, file2):
    """Compares if two files have the same contents using checksum.

        Args:
            file1: The path for the first file to compare.
            file2: The path for the second file to compare.

        Returns:
            True if files have the same content. False otherwise.
    """
    return get_checksum(file1) == get_checksum(file2)


if __name__ == '__main__':
    unittest.main()
