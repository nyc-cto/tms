import os.path
import sys
from git import Repo

# Path to root project git (if needed)
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
PROJECT_ROOT_GIT_PATH = f'{ROOT_PATH}/.git'

# Log messages to be printed by git_push
NO_CHANGES_MESSAGE = "No changes detected\n"
DEBUGGING_MESSAGE = "Skipping git push because it's disabled for debugging\n"
PUSHING_MESSAGE = "Pushing files to shared repository\n"
PUSH_SUCCESSFUL_MESSAGE = "Push successful\n"


# Push shared repository to Git if any files changed
def git_push(git_repo_path, commit_message="Update shared repository", enable_push=True, log=sys.stdout):
    """Utility method that pushes any updates to the shared_directory subdirectory of a git repo.

        Args:
            git_repo_path: The git repo path where the push should happen.
            commit_message: A string with the message for committing the changes to the git repo.
            enable_push: Boolean. Default to True to enable pushing to git repo. Set to False for testing.
            log: Where to print messages. Default is to stdout.
    """
    repo = Repo(git_repo_path)

    t = repo.head.commit.tree
    repo.index.add(["shared_directory"])
    if repo.git.diff(t):
        repo.index.commit(commit_message)
        if enable_push:
            log.write(PUSHING_MESSAGE)
            branch_name = repo.active_branch.name
            repo.git.push('origin', branch_name)
            log.write(PUSH_SUCCESSFUL_MESSAGE)
        else:
            log.write(DEBUGGING_MESSAGE)
    else:
        log.write(NO_CHANGES_MESSAGE)

    repo.close()
