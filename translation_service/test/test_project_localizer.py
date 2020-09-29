import tempfile
import unittest
import sys
import os
import shutil
sys.path.append('src')
import project_localizer
from translators import TranslatorFactory


EXAMPLE_FILE = 'example.po'
GOLDEN_EXAMPLE_IN = 'golden_in.po'
GOLDEN_EXAMPLE_OUT = 'golden_out.po'
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
TARGET_LANGUAGE_ISO_LIST = ['es', 'fr']


class TestPoLocalizer(unittest.TestCase):

    # Temporary directories  to use during testing
    temp_root_dir = None

    @classmethod
    def setUpClass(cls):
        # Make a temporary root directory
        cls.temp_root_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        # Remove temporary root directory and its subdirectories & files
        shutil.rmtree(cls.temp_root_dir)

    def test_localize_project(self):
        """ Test for localize_project()

            setup: input_dir must hold language subdirs with .po files inside.

            file modifications: localization subdirs created in output_dir

            expected args: input_dir, output_dir, translation_api, google_key_path
            expected returns: (None)
        """
        # ------------ Setup -------------

        # Make temporary in/out directories to hold the test resources in
        temp_in_dir = os.path.join(self.temp_root_dir, 'in')
        temp_out_dir = os.path.join(self.temp_root_dir, 'out')

        if not os.path.exists(temp_in_dir):
            os.makedirs(temp_in_dir)

        if not os.path.exists(temp_out_dir):
            os.makedirs(temp_out_dir)

        # Get the path for the golden in example file
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)

        # Create subdirectories for each target language
        # and add a copy of the golden in example file in each
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_in_dir, lang)
            if not os.path.exists(lang_subdir):
                os.makedirs(lang_subdir)

            # Copy the golden in example file into the lang_subdir
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)
            shutil.copyfile(golden_in_filepath, lang_subdir_example_path)

        # ------------ Run localize_project -------------

        # Call localize_project with the test input and output directories
        project_localizer.localize_project(temp_in_dir, temp_out_dir, translation_api='caps')

        # TEST: Check that all localization subdirectories are created in the output dir
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_out_dir, lang)
            self.assertTrue(os.path.exists(lang_subdir))

    def test_localize_po_file(self):
        """ Test for localize_po_file()

            setup:
                - in_path must hold a po_file inside
                - translator must be a CapsTranslator object

            file modifications: localized po_file written to out_path

            expected args: in_path, out_path, po_file (golden), target_lang_iso, translator
            expected returns: (None)
        """
        # ------------ Setup -------------

        # Make temporary in/out directories to hold the test resources in
        temp_in_dir = os.path.join(self.temp_root_dir, 'in')
        temp_out_dir = os.path.join(self.temp_root_dir, 'out')

        if not os.path.exists(temp_in_dir):
            os.makedirs(temp_in_dir)

        if not os.path.exists(temp_out_dir):
            os.makedirs(temp_out_dir)

        # Get the path for the golden in example file
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)

        # Copy the golden in example file into the in directory
        example_path = os.path.join(temp_in_dir, EXAMPLE_FILE)
        shutil.copyfile(golden_in_filepath, example_path)

        # Language code for testing
        lang = TARGET_LANGUAGE_ISO_LIST[0]

        # Create a translator object that does capitalization
        translator = TranslatorFactory.get_translator(translation_api='caps')

        # ------------ Run po_localizer -------------

        # Call po_localizer
        project_localizer.localize_po_file(temp_in_dir, temp_out_dir, EXAMPLE_FILE, lang, translator)

        # Get path for where the out file is expected to be written
        out_example_filepath = os.path.join(temp_out_dir, EXAMPLE_FILE)

        # TEST: Ensure the cycle is completed and a file is written in the correct location
        self.assertTrue(os.path.exists(out_example_filepath))

    def test_create_output_localized_subdir(self):
        """ Test for create_output_localized_subdir()

            setup: output_dir must exist.

            file modifications: subdir for target_lang_iso created in output_dir

            expected args: output_dir, target_lang_iso
            expected returns: (None)
        """
        # ------------ Setup -------------

        # Make temporary out directory
        temp_out_dir = os.path.join(self.temp_root_dir, 'out')

        if not os.path.exists(temp_out_dir):
            os.makedirs(temp_out_dir)

        # Language subdir and path for testing
        lang = TARGET_LANGUAGE_ISO_LIST[0]
        lang_subdir = os.path.join(temp_out_dir, lang)

        # ------------ run create_output_locacalized_subdir -------------

        # Call create_output_localized_subdir
        project_localizer.create_output_localized_subdir(temp_out_dir, lang)

        # TEST: Ensure that lang_subdir is created
        self.assertTrue(os.path.exists(lang_subdir))


if __name__ == '__main__':
    unittest.main()
