import filecmp
import os
import shutil
import sys
import tempfile
import unittest
sys.path.append('src')
from po_file import MsgElement
from po_file import PoFile
from translators import TranslatorFactory

GOLDEN_PO_MSGID = ['msgid "We can use machine translation to get many localizations "',
                   '"done automatically and quickly."']
GOLDEN_PO_MSGID_TEXT = "We can use machine translation to get many localizations done automatically and quickly."
GOLDEN_PO_TRANSLATION = ["WE CAN USE MACHINE TRANSLATION TO GET MANY LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."]
GOLDEN_PO_MSGSTR = ['msgstr "WE CAN USE MACHINE TRANSLATION TO GET MANY LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."']

GOLDEN_PO_HEADER = ['msgid ""',
                    'msgstr ""',
                    '"Content-Type: text/plain; charset=UTF-8\\n"',
                    '"Content-Transfer-Encoding: 8bit\\n"',
                    '"Language: de\\n"',
                    '"Generated-By: Serge 1.4\\n"']
GOLDEN_PO_MSGHEADER_LISTS = [['#. /about',
                              '#: File: sample.json',
                              '#: ID: a5eea87543a1a8fad51039d72f407011'],
                             ['#. /title',
                              '#: File: sample.json',
                              '#: ID: b5eea87543a1a8fad51039d72f407011']]
GOLDEN_PO_MSGID_LISTS = [['msgid "Let\'s get things translated!"'],
                         ['msgid "We can use machine translation to get many localizations "',
                         '"done automatically and quickly."']]
GOLDEN_PO_MSGSTR_LISTS = [['msgstr "LET\'S GET THINGS TRANSLATED!"'], ['msgstr ""']]
GOLDEN_PO_MSGSTR_TRANSLATED_LISTS = [['msgstr "LET\'S GET THINGS TRANSLATED!"'],
                                     ['msgstr "WE CAN USE MACHINE TRANSLATION TO GET MANY '
                                      'LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."']]

EXAMPLE_FILE = 'example.po'
GOLDEN_EXAMPLE_IN = 'golden_in.po'
GOLDEN_EXAMPLE_OUT = 'golden_out.po'
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
TARGET_LANGUAGE_ISO = 'es'


class TestPoFile(unittest.TestCase):
    # Temporary directories & files to read/write during testing
    temp_root_dir = None
    temp_in_dir = None
    temp_out_dir = None
    in_example_filepath = None

    @classmethod
    def setUpClass(cls):

        # Make a temporary root directory and inbox/outbox subdirectories to hold the test resources in
        cls.temp_root_dir = tempfile.mkdtemp()
        cls.temp_in_dir = os.path.join(cls.temp_root_dir, 'in')
        cls.temp_out_dir = os.path.join(cls.temp_root_dir, 'out')

        if not os.path.exists(cls.temp_in_dir):
            os.makedirs(cls.temp_in_dir)

        if not os.path.exists(cls.temp_out_dir):
            os.makedirs(cls.temp_out_dir)

        # Copy the golden file into the temporary directory inbox
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)
        cls.in_example_filepath = os.path.join(cls.temp_in_dir, EXAMPLE_FILE)
        shutil.copyfile(golden_in_filepath, cls.in_example_filepath)

    @classmethod
    def tearDownClass(cls):
        # Remove temporary root directory and its subdirectories & files
        shutil.rmtree(cls.temp_root_dir)

    def test_get_msgid_text(self):
        """
        Test for MsgElement.get_msgid_text()

            setup: MsgElement must be initialized with msgid
            object modifications: (None)

            expected args: (None)
            expected returns: string with concatenated contents of the MsgElement's msgid list

        """
        # Initialize test element with the Golden msgids
        elem = MsgElement(["#. /about"], GOLDEN_PO_MSGID, ['msgstr ""'])

        # TEST: Compare the returned string and the Golden version
        self.assertEqual(elem.get_msgid_text(), GOLDEN_PO_MSGID_TEXT)

    def test_add_msgstr_translation(self):
        """
        Test for MsgElement.add_msgstr_translation()

            setup: MsgElement must be initialized with msgid
            object modifications: MsgElement.msgstr will be set to the translation_list

            expected args: translation_list (a list of translations of the msgid)
            expected returns: (None)
        """

        # Initialize test element with the Golden msgids
        elem = MsgElement(["#. /about"], GOLDEN_PO_MSGID, ['msgstr ""'])

        # Add translation
        elem.add_msgstr_translation(GOLDEN_PO_TRANSLATION)

        # TEST: Compare msgstr with Golden
        self.assertEqual(elem.msgstr, GOLDEN_PO_MSGSTR)

        # TEST: Ensure msgstr_translated is set to True
        self.assertTrue(elem.msgstr_translated)

    def test_parse_po_file(self):
        """
        Test for PoFile.parse_po_file()

            setup: PoFile must be initialized with po_filepath
            object modifications: PoFile.header and PoFile.msg_elements will be filled based on file contents

            expected args: (None)
            expected returns: (None)

        """

        # Initialize PoFile object
        po = PoFile(self.in_example_filepath)
        po.parse_po_file()

        # TEST: Compare header and golden header
        self.assertEqual(po.header, GOLDEN_PO_HEADER)

        # TEST: Compare each msg_element's msgheader, msgid, and msgstr
        i = 0
        for elem in po.msg_elements:
            self.assertEqual(elem.msgheader, GOLDEN_PO_MSGHEADER_LISTS[i])
            self.assertEqual(elem.msgid, GOLDEN_PO_MSGID_LISTS[i])
            self.assertEqual(elem.msgstr, GOLDEN_PO_MSGSTR_LISTS[i])
            i += 1

    def test_translate_po_file(self):
        """
        Test for PoFile.translate_po_file()

            setup: PoFile must be initialized with po_filepath, header, and msg_elements
            object modifications: PoFile.msg_elements will be updated with translated msgstr

            expected args: target_lang_iso (translation language code), translator (Translator object)
            expected returns: (None)

        """

        # Create a translator object that does capitalization
        translator = TranslatorFactory.get_translator(translation_api='caps')

        # Initialize PoFile object
        po = PoFile(self.in_example_filepath)

        # PoFile must be initialized with golden po_filepath, header, and msg_elements
        po.header = GOLDEN_PO_HEADER
        msg_elements = []
        for i in range(len(GOLDEN_PO_MSGHEADER_LISTS)):
            elem = MsgElement(GOLDEN_PO_MSGHEADER_LISTS[i], GOLDEN_PO_MSGID_LISTS[i], GOLDEN_PO_MSGSTR_LISTS[i])
            msg_elements.append(elem)
        po.msg_elements = msg_elements

        po.translate_po_file(TARGET_LANGUAGE_ISO, translator)

        # TEST: Compare each msg_element's msgstr to golden translated msgstrs
        i = 0
        for elem in po.msg_elements:
            self.assertEqual(elem.msgstr, GOLDEN_PO_MSGSTR_TRANSLATED_LISTS[i])
            i += 1

    def test_write_localized_po_file(self):
        """
        Test for PoFile.write_localized_po_file()

            setup: PoFile must be initialized with po_filepath, header, and msg_elements
            object modifications: (None)

            file modifications: File will be written to localized_po_filepath will contents of PoFile object

            expected args: localized_po_filepath (path of where to write the localized file to)
            expected returns: (None)

        """

        # Initialize PoFile object
        po = PoFile(self.in_example_filepath)

        # PoFile must be initialized with golden po_filepath, header, and msg_elements
        po.header = GOLDEN_PO_HEADER
        msg_elements = []
        for i in range(len(GOLDEN_PO_MSGHEADER_LISTS)):
            elem = MsgElement(GOLDEN_PO_MSGHEADER_LISTS[i], GOLDEN_PO_MSGID_LISTS[i],
                              GOLDEN_PO_MSGSTR_TRANSLATED_LISTS[i])
            msg_elements.append(elem)
        po.msg_elements = msg_elements

        # Get path for golden_out comparison file
        golden_out_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_OUT)

        # Get path for where to write out file
        out_example_filepath = os.path.join(self.temp_out_dir, EXAMPLE_FILE)

        # Call write_localized_po_file to write to the out_example_filepath
        po.write_localized_po_file(out_example_filepath)

        # TEST: Use checksum to ensure the file written out matches the golden file
        self.assertTrue(filecmp.cmp(out_example_filepath, golden_out_filepath))


if __name__ == '__main__':
    unittest.main()
