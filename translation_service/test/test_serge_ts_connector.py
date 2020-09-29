import filecmp
import tempfile
import unittest
import sys
import os
import shutil
sys.path.append('src')
import serge_ts_connector

EXAMPLE_FILE = 'example.po'
GOLDEN_EXAMPLE_IN = 'golden_in.po'
GOLDEN_EXAMPLE_OUT = 'golden_out.po'
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
TARGET_LANGUAGE_ISO_LIST = ['es', 'fr']
MODES = ["push_ts", "pull_ts"]


class TestSergeTsConnector(unittest.TestCase):

    # Temporary directories & files to read/write during testing
    temp_root_dir = None

    @classmethod
    def setUpClass(cls):

        # Make a temporary root directory
        cls.temp_root_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        # Remove temporary root directory and its subdirectories & files
        shutil.rmtree(cls.temp_root_dir)

    def test_serge_push_ts(self):
        """ Test for serge_push_ts()

            setup: serge_ts directory must hold language subdirs with .po files inside.

            file modifications:
                - Copies of subdirs and .po files from serge_ts will be added to ts_serge_copy.
                - A localized version of those subdirs & .po files will be added to the ts_outbox.
                - ts_inbox will be created and deleted.

            expected args: serge_ts, ts_serge_copy, ts_inbox, ts_outbox, translation_api, google_key_path
            expected returns: (None)
        """
        # ------------ Setup -------------

        # Make temporary directories to hold the test resources in
        temp_serge_ts = os.path.join(self.temp_root_dir, 'serge_ts')
        temp_ts_serge_copy = os.path.join(self.temp_root_dir, 'ts_serge_copy')
        temp_ts_inbox = os.path.join(self.temp_root_dir, 'ts_inbox')
        temp_ts_outbox = os.path.join(self.temp_root_dir, 'ts_outbox')

        if not os.path.exists(temp_serge_ts):
            os.makedirs(temp_serge_ts)
        if not os.path.exists(temp_ts_serge_copy):
            os.makedirs(temp_ts_serge_copy)
        if not os.path.exists(temp_ts_inbox):
            os.makedirs(temp_ts_inbox)
        if not os.path.exists(temp_ts_outbox):
            os.makedirs(temp_ts_outbox)

        # Get the path for the golden in example file
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)

        # Create subdirectories in temp_serge_ts for each target languages
        # and add a copy of the golden in example file in each
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_serge_ts, lang)
            if not os.path.exists(lang_subdir):
                os.makedirs(lang_subdir)

            # Copy the golden in example file into the lang_subdir
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)
            shutil.copyfile(golden_in_filepath, lang_subdir_example_path)

        # Get the path for the golden out example file
        golden_out_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_OUT)

        # ------------ Run serge_push_ts -------------

        serge_ts_connector.serge_push_ts(temp_serge_ts, temp_ts_serge_copy, temp_ts_inbox, temp_ts_outbox,
                                         translation_api='caps', google_key_path=None)

        # TEST: Check that the temp_ts_serge_copy example files match the golden in files
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_ts_serge_copy, lang)

            # Get the example file path
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)

            # Use checksum to ensure the file matches the golden in file
            self.assertTrue(filecmp.cmp(lang_subdir_example_path, golden_in_filepath))

        # TEST: Check that the temp_ts_outbox example files match the golden out files
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_ts_outbox, lang)

            # Get the example file path
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)

            # Use checksum to ensure the file matches the golden out file
            self.assertTrue(filecmp.cmp(lang_subdir_example_path, golden_out_filepath))

    def test_serge_pull_ts(self):
        """ Test for serge_pull_ts()

            setup:
                - serge_ts directory must hold language subdirs with .po files inside.
                - ts_outbox must hold any localized versions of the .po files in their respective subdirs.

            file modifications:
                - Copies of subdirs and .po files from ts_outbox will be added/overwritten to serge_ts.
                - Outbox will be deleted.

            expected args: serge_ts, ts_outbox
            expected returns: (None)
        """
        # ------------ Setup -------------

        # Make temporary directories to hold the test resources in
        temp_serge_ts = os.path.join(self.temp_root_dir, 'serge_ts')
        temp_ts_outbox = os.path.join(self.temp_root_dir, 'ts_outbox')

        if not os.path.exists(temp_serge_ts):
            os.makedirs(temp_serge_ts)
        if not os.path.exists(temp_ts_outbox):
            os.makedirs(temp_ts_outbox)

        # Get the path for the golden in example file
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)

        # Create subdirectories in temp_serge_ts for each target languages
        # and add a copy of the golden in example file in each
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_serge_ts, lang)
            if not os.path.exists(lang_subdir):
                os.makedirs(lang_subdir)

            # Copy the golden in example file into the lang_subdir
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)
            shutil.copyfile(golden_in_filepath, lang_subdir_example_path)

        # Get the path for the golden out example file
        golden_out_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_OUT)

        # Create subdirectories in ts_outbox for each target languages
        # and add a copy of the golden out example file in each
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_ts_outbox, lang)
            if not os.path.exists(lang_subdir):
                os.makedirs(lang_subdir)

            # Copy the golden out example file into the lang_subdir
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)
            shutil.copyfile(golden_out_filepath, lang_subdir_example_path)

        # ------------ Run serge_pull_ts -------------

        serge_ts_connector.serge_pull_ts(temp_serge_ts, temp_ts_outbox)

        # TEST: Check that the temp_serge_ts example files have been overwritten with the golden out file
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(temp_serge_ts, lang)

            # Get the example file path
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)

            # Use checksum to ensure the file matches the golden out file
            self.assertTrue(filecmp.cmp(lang_subdir_example_path, golden_out_filepath))

    def test_validate_args_invalid_dir(self):
        """
        validate_args
            expected_in: mode, serge_dir
            expected_out: Error for invalid serge_dir
        """

        serge_dir_invalid = ""

        # TEST: Error is raised if the serge_dir is invalid
        with self.assertRaises(serge_ts_connector.InvalidArgumentError):
            serge_ts_connector.validate_args(MODES[0], serge_dir_invalid)

    def test_validate_args_invalid_mode(self):
        """
        validate_args
            expected_in: mode, serge_dir
            expected_out: Error for invalid mode
        """
        # Make temporary serge directory
        temp_serge_dir = os.path.join(self.temp_root_dir, 'serge')

        if not os.path.exists(temp_serge_dir):
            os.makedirs(temp_serge_dir)

        # TEST: Error is raised if the mode is invalid
        with self.assertRaises(serge_ts_connector.InvalidArgumentError):
            serge_ts_connector.validate_args('invalid_mode', temp_serge_dir)


if __name__ == '__main__':
    unittest.main()
