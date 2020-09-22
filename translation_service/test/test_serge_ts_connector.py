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


class TestSergeTsConnector(unittest.TestCase):

    # Temporary directories & files to read/write during testing
    temp_root_dir = None
    temp_in_dir = None
    temp_out_dir = None

    @classmethod
    def setUpClass(cls):

        # Make a temporary root directory and in/out subdirectories to hold the test resources in
        cls.temp_root_dir = tempfile.mkdtemp()
        cls.temp_in_dir = os.path.join(cls.temp_root_dir, 'in')
        cls.temp_out_dir = os.path.join(cls.temp_root_dir, 'out')

        if not os.path.exists(cls.temp_in_dir):
            os.makedirs(cls.temp_in_dir)

        if not os.path.exists(cls.temp_out_dir):
            os.makedirs(cls.temp_out_dir)

        # Get the path for the golden in example file
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)

        # Create subdirectories for each target language
        # and add a copy of the golden in example file in each
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(cls.temp_in_dir, lang)
            if not os.path.exists(lang_subdir):
                os.makedirs(lang_subdir)

            # Copy the golden in example file into the lang_subdir
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)
            shutil.copyfile(golden_in_filepath, lang_subdir_example_path)

    @classmethod
    def tearDownClass(cls):
        # Remove temporary root directory and its subdirectories & files
        shutil.rmtree(cls.temp_root_dir)

    # TODO: Change validation tests to work with serge_ts_connector args
    def test_validate_args_invalid_in(self):
        """
        validate_args
            expected_in: input_dir, output_dir
            expected_out: Error for invalid input_dir
        """

        input_dir_invalid = ""

        # TEST: Error is raised if the input_dir is invalid
        with self.assertRaises(serge_ts_connector.InvalidArgumentError):
            serge_ts_connector.validate_args(input_dir_invalid, self.temp_out_dir)

    def test_validate_args_invalid_out(self):
        """
        validate_args
            expected_in: input_dir, output_dir
            expected_out: Error for invalid output_dir
        """
        output_dir_invalid = ""

        # TEST: Error is raised if the output_dir is invalid
        with self.assertRaises(serge_ts_connector.InvalidArgumentError):
            serge_ts_connector.validate_args(self.temp_in_dir, output_dir_invalid)


if __name__ == '__main__':
    unittest.main()
