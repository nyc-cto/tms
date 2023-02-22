import io
import os
import shutil
import sys
import tempfile
import unittest
from git import Repo
sys.path.append('src')
import utils


class TestUtils(unittest.TestCase):

    # Temporary directory to use during testing
    temp_root_dir = None

    @classmethod
    def setUpClass(cls):

        # Make a temporary root directory and shared_directory subdir
        cls.temp_root_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        # Remove temporary root directory and its subdirectories & files
        shutil.rmtree(cls.temp_root_dir)

    def test_git_push_no_changes(self):

        # Create a directory for this test
        test_dir = os.path.join(self.temp_root_dir, 'test_git_push_no_changes')
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)

        # Create a shared_directory for files inside this test_dir
        shared_directory = os.path.join(test_dir, 'source_files/en')
        if not os.path.exists(shared_directory):
            os.makedirs(shared_directory)

        # Set up a git repository to use during testing
        temp_repo = Repo.init(test_dir)

        # Create a dummy file and commit it to start the repo history
        f = os.path.join(test_dir, "DUMMY")
        open(f, 'wb').close()
        temp_repo.index.add([f])
        temp_repo.index.commit("FOO")

        # Call git_push using the test_dir and have it write to the log
        log = io.StringIO()
        utils.git_push(test_dir, log=log, enable_push=False)

        # Close the repo
        temp_repo.close()

        # TEST: When no uncommited changes have been made to the repo,
        #       it logs the NO_CHANGES_MESSAGE
        self.assertEqual(log.getvalue(), utils.NO_CHANGES_MESSAGE)

    def test_git_push_with_changes(self):

        # Create a directory for this test
        test_dir = os.path.join(self.temp_root_dir, 'test_git_push_with_changes')
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)

        # Create a shared_directory for files inside this test_dir
        shared_directory = os.path.join(test_dir, 'source_files/en')
        if not os.path.exists(shared_directory):
            os.makedirs(shared_directory)

        # Set up a git repository to use during testing
        temp_repo = Repo.init(test_dir)

        # Create a dummy file and commit it to start the repo history
        f = os.path.join(test_dir, "DUMMY")
        open(f, 'wb').close()
        temp_repo.index.add([f])
        temp_repo.index.commit("FOO")

        # Add a file to the shared_directory WITHOUT committing
        uncommited_file = os.path.join(shared_directory, "uncommitted_file")
        open(uncommited_file, 'wb').close()
        temp_repo.index.add([uncommited_file])

        # Call git_push using the test_dir and have it write to the log
        log = io.StringIO()
        utils.git_push(test_dir, log=log, enable_push=False)

        # Close the repo
        temp_repo.close()

        # TEST: When uncommited changes have been made to the repo,
        #       it logs the DEBUGGING_MESSAGE
        self.assertEqual(log.getvalue(), utils.DEBUGGING_MESSAGE)

if __name__ == '__main__':
    unittest.main()