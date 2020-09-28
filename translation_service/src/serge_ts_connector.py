import argparse
import filecmp
import os
import shutil
import sys
sys.path.append('src')
from project_localizer import localize_project

# Append path to utils package before importing it
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
utils_path = f'{root_path}/common/src'
sys.path.append(utils_path)


def serge_push_ts(serge_ts, ts_serge_copy, ts_inbox, ts_outbox, translation_api, google_key_path):
    """Handles the Serge push_ts command. Copies .po files from serge_ts that are new/updated
        (compares to those in the ts_serge_copy) to both ts_serge_copy (local copy) and ts_inbox (files to process).
        Also localizes all the language subdirs in the ts_inbox and writes to the ts_outbox.
        NOTE: This will also copy over any files that have been previously localized and pushed to Serge since
            Serge will change the line breaks in any localized msgstr, requiring update on the part of ts_serge_copy,
            causing the files to go through the localization process once more, although none of the strings will be
            retranslated (simply parsed and then rewritten to the ts_outbox).

        Args:
            serge_ts: The path to the directory where Serge has the .po files that need translation.
            ts_serge_copy: The path to the translation service's directory of local copies of serge .po files
                to add any new/updated files to.
            ts_inbox: The path to the translation service inbox (files to process) to copy the files to.
            ts_outbox: The path to the outbox dir where to write localized language subdirs and files.
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile (not required if not using this API).
    """
    # Get a list of all the subdirs in serge_translation_dir
    subdirs = [subdir for subdir in os.listdir(serge_ts)
               if os.path.isdir(os.path.join(serge_ts, subdir))]

    # TODO: Future: See if there is a better way to handle this (git diff?)
    # TODO: Future: Think about how to handle orphaned files (no longer exist on Serge side)
    # Create all subdirs (if they don't already exist) in both ts_serge_po_dir and ts_inbox
    # and copy any new/updated files as well
    for subdir in subdirs:

        subdir_path = os.path.join(serge_ts, subdir)

        # Create the subdir if it doesn't already exist in ts_serge_po_dir and ts_inbox
        ts_serge_subdir_path = os.path.join(ts_serge_copy, subdir)
        ts_inbox_subdir_path = os.path.join(ts_inbox, subdir)
        if not os.path.exists(ts_serge_subdir_path):
            os.makedirs(ts_serge_subdir_path)
        if not os.path.exists(ts_inbox_subdir_path):
            os.makedirs(ts_inbox_subdir_path)

        # Get a list of all files in this subdir
        # Note: Assumes there are no further nested subdirectories
        files = os.listdir(subdir_path)

        # Copy any new/updated files from serge_translation_dir to both ts_serge_po_dir and ts_inbox
        for file in files:

            # Make file paths for each subdir
            serge_file_path = os.path.join(subdir_path, file)
            ts_serge_file_path = os.path.join(ts_serge_subdir_path, file)
            ts_inbox_file_path = os.path.join(ts_inbox_subdir_path, file)

            # Check if the file is new (doesn't exist in ts_serge_po_dir)
            if not os.path.exists(ts_serge_file_path):
                # File is new, add a copy to both ts_serge_po_dir and ts_inbox
                shutil.copy2(serge_file_path, ts_serge_file_path)
                shutil.copy2(serge_file_path, ts_inbox_file_path)
            else:
                # File exists; check if updated from current version in ts_serge_po_dir
                if not filecmp.cmp(serge_file_path, ts_serge_file_path):

                    # File is updated, copy/overwrite ts_serge_po_dir and ts_inbox
                    shutil.copy2(serge_file_path, ts_serge_file_path)
                    shutil.copy2(serge_file_path, ts_inbox_file_path)

    # Localize the project and its po files
    localize_project(ts_inbox, ts_outbox, translation_api, google_key_path)

    # Remove all contents from inbox once processed (localized)
    shutil.rmtree(ts_inbox)


def serge_pull_ts(serge_ts, ts_outbox):
    """Handles the Serge push_ts command. Copies the localized .po files from ts_outbox into serge_ts.

        Args:
            serge_ts: The path to the directory where Serge has the .po files that need updating.
            ts_outbox: The path to the translation service outbox where the localized .po files are.
    """

    # Get a list of all the subdirs in ts_outbox
    subdirs = [subdir for subdir in os.listdir(ts_outbox)
               if os.path.isdir(os.path.join(ts_outbox, subdir))]

    # Copy/Overwrite all files from all subdirs in ts_outbox to respective subdirs in serge_translation_dir
    for subdir in subdirs:

        ts_outbox_subdir_path = os.path.join(ts_outbox, subdir)

        # Get the subdir paths for where to copy to in serge
        serge_subdir_path = os.path.join(serge_ts, subdir)

        # Get a list of all files in this subdir
        # Note: Assumes there are no further nested subdirectories
        files = os.listdir(ts_outbox_subdir_path)

        # Copy/Overwrite files from ts_outbox to serge_translation_dir
        for file in files:

            # Make file paths for each subdir
            ts_outbox_file_path = os.path.join(ts_outbox_subdir_path, file)
            serge_file_path = os.path.join(serge_subdir_path, file)

            # Copy/Overwrite
            shutil.copy2(ts_outbox_file_path, serge_file_path)

    # Remove all contents from outbox once processed (copied to Serge)
    shutil.rmtree(ts_outbox)


def validate_args(mode, serge_dir):
    """Validates the arguments for this program. Exits with message if any invalid args.

        Args:
            mode: The mode to connect to Serge (push_ts or pull_ts)
            serge_dir: Filepath for the serge/ts/ directory with the .po files.
    """
    MODES = ["push_ts", "pull_ts"]

    # Check that a valid mode is provided
    if mode not in MODES:
        raise InvalidArgumentError("ERROR: Invalid mode. (Modes = {})".format(MODES))

    # Check that the serge directory exists
    if not os.path.isdir(serge_dir):
        raise InvalidArgumentError("ERROR: Serge directory does not exist.")


class InvalidArgumentError(Exception):
    """Error Handler for invalid arguments.

        Attributes:
            message: The error message to display
    """

    def __init__(self, message):
        self.message = message


# TODO: Future: Add ability to have project subdirectory structure (possibly via Serge config, possibly this program)
def main():
    """Program that connects Serge with a translation service, handling Serge push-ts and pull-ts."""

    # Paths for each directory based on environment variables
    SERGE_TS = os.environ['SERGE_TS']
    TS_SERGE_COPY = os.environ['TS_SERGE_COPY']
    TS_INBOX = os.environ['TS_INBOX']
    TS_OUTBOX = os.environ['TS_OUTBOX']

    parser = argparse.ArgumentParser(description='Handles push-ts and pull-ts for Serge.')

    parser.add_argument("--mode", help="mode is either push_ts or pull_ts", required=True)
    parser.add_argument("--serge_dir", help="filepath for serge/ts/ directory with .po files. Default={}".format(
        SERGE_TS), default=SERGE_TS)
    parser.add_argument("--ts_serge_dir", help="filepath for translation_service copy of serge/ts/. Default={}".format(
        TS_SERGE_COPY), default=TS_SERGE_COPY)
    parser.add_argument("--ts_inbox", help="filepath for translation_service inbox directory. Default={}".format(
        TS_INBOX), default=TS_INBOX)
    parser.add_argument("--ts_outbox", help="filepath for translation_service outbox directory. Default={}".format(
        TS_OUTBOX), default=TS_OUTBOX)
    parser.add_argument('--translation_api', type=str,
                        help='translation API to use ("google" for Google Translate,'
                             ' "caps" for capitalization). Default=caps', default='caps')
    parser.add_argument('--google_key_path', type=str,
                        help='path for the Google Service Account JSON keyfile', required=False)

    args = parser.parse_args()

    # Normalize paths
    args.serge_dir = os.path.normpath(args.serge_dir)
    args.ts_serge_dir = os.path.normpath(args.ts_serge_dir)
    args.ts_inbox = os.path.normpath(args.ts_inbox)
    args.ts_outbox = os.path.normpath(args.ts_outbox)

    # Validate arguments for this program
    # Note that arguments for the Translator (translation_api and google_key_path) will be validated separately
    try:
        validate_args(args.mode, args.serge_dir)
    except InvalidArgumentError as error:
        sys.exit(error.message)

    # Create ts_serge_dir, ts_inbox, ts_outbox if they don't already exist
    if not os.path.exists(args.ts_serge_dir):
        os.makedirs(args.ts_serge_dir)
    if not os.path.exists(args.ts_inbox):
        os.makedirs(args.ts_inbox)
    if not os.path.exists(args.ts_outbox):
        os.makedirs(args.ts_outbox)

    # TODO: Future: Handle the case where push_ts is being called before the localization cycle is complete;
    #   potentially solve via multiple time-stamped inboxes (or replace with queues)

    if args.mode == 'push_ts':
        serge_push_ts(serge_ts=args.serge_dir, ts_serge_copy=args.ts_serge_dir,
                      ts_inbox=args.ts_inbox, ts_outbox=args.ts_outbox,
                      translation_api=args.translation_api, google_key_path=args.google_key_path)
    else:
        serge_pull_ts(serge_ts=args.serge_dir, ts_outbox=args.ts_outbox)


if __name__ == "__main__":
    main()
