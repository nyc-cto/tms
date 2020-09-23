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

    def test_copy_serge_po_files(self):
        """TODO: stub test for copy_serge_po_files function."""
        pass

    def test_copy_outbox_to_serge(self):
        """TODO: stub test for copy_outbox_to_serge function."""
        pass

    def test_localize(self):
        """TODO: stub test for localize function."""
        pass

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
