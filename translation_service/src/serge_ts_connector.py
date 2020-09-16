import argparse
import os
import shutil
import sys
sys.path.append('src')
from project_localizer import localize_project

SERGE_TRANSLATION_DIR = '/var/serge/data/ts'
TS_INBOX = '/shared_directory/po/inbox'  # TODO: Put in git repo shared_dir
TS_OUTBOX = '/shared_directory/po/outbox'

# TODO: Decide where to put git checkouts & commits
#   Likely at beginning and end of each step: copy_serge, localize, copy_outbox


# TODO: get to work with google translate (perhaps have this as part of serge config?)
def copy_serge_and_localize(serge_translation_dir=SERGE_TRANSLATION_DIR, ts_inbox=TS_INBOX, ts_outbox=TS_OUTBOX,
                            translation_api='caps', google_key_path=None):
    """Copies the subtree for the serge_translation_dir into the inbox and calls localize.

        Args:
            serge_translation_dir: The path to the directory where Serge has the .po files that need translation.
            ts_inbox: The path to the translation service inbox to copy the files to.
            ts_outbox: The path to the outbox dir where to put localized language subdirs and files.
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile (not required if not using this API).
    """
    # TODO: Likely separate this out into separate copy and localize steps

    # TODO: Have copy write to a shared_directory/po_files/serge dir (add this as an arg) for any files that
    #  were updated on Serge's ts/ dir and then only write those updated files to the inbox

    # TODO: Decide how to handle if the directory already exists. For now, delete!
    if os.path.exists(ts_inbox):
        shutil.rmtree(ts_inbox)

    # Use shutil to copy all the directories and files from serge_translation_dir to ts_inbox
    shutil.copytree(serge_translation_dir, ts_inbox)

    # Localize everything in the inbox to the outbox
    localize(ts_inbox, ts_outbox, translation_api, google_key_path)


def copy_outbox_to_serge(serge_translation_dir=SERGE_TRANSLATION_DIR, ts_outbox=TS_OUTBOX):
    """Copies the subtree for the outbox (with localized files) into the serge_translation_dir.

        Args:
            serge_translation_dir: The path to the directory where Serge has the .po files that need translation.
            ts_outbox: The path to the translation service inbox to copy the files to.
    """
    # TODO: Decide how to handle if the directory already exists. For now, delete!
    if os.path.exists(serge_translation_dir):
        shutil.rmtree(serge_translation_dir)

    # Use shutil to copy all the directories and files from ts_outbox to serge_translation_dir
    shutil.copytree(ts_outbox, serge_translation_dir)

    # TODO: Decide if this is how it should be handled
    # Remove all contents from outbox, then recreate the outbox
    shutil.rmtree(ts_outbox)
    os.makedirs(ts_outbox)


# TODO: Handle more complex subdir structure?
def localize(ts_inbox=TS_INBOX, ts_outbox=TS_OUTBOX, translation_api='caps', google_key_path=None):
    """Localizes all the language subdirs in the ts_inbox and writes to the ts_outbox.

        Args:
            ts_inbox: The path to the inbox dir with language subdirs and files that need to be localized.
            ts_outbox: The path to the outbox dir where to put localized language subdirs and files.
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile (not required if not using this API).
    """
    # Normalize paths  # TODO: See if needed
    # args.input_dir, args.output_dir = os.path.normpath(args.input_dir), os.path.normpath(args.output_dir)

    # Localize the project and its po files
    localize_project(ts_inbox, ts_outbox, translation_api, google_key_path)

    # TODO: Decide if this is how it should be handled
    # Remove all contents from inbox, then recreate the inbox
    shutil.rmtree(ts_inbox)
    os.makedirs(ts_inbox)


def main():
    """Localizes all .po files from an input project directory into an output project directory."""
    parser = argparse.ArgumentParser(description='Handles push-ts and pull-ts for Serge.')
    # TODO: Decide if all the arguments should be passed in here as part of the Serge config calling them
    # parser.add_argument("--input_dir", help="filepath for input project directory", required=True)
    # parser.add_argument("--output_dir", help="filepath for output project directory", required=True)
    # parser.add_argument('--translation_api', type=str,
    #                     help='translation API to use ("google" for Google Translate,'
    #                          ' "caps" for capitalization)', required=True)
    # parser.add_argument('--google_key_path', type=str,
    #                     help='path for the Google Service Account JSON keyfile', required=False)

    parser.add_argument("--mode", help="mode is either push_ts or pull_ts", required=True)
    args = parser.parse_args()

    # TODO: Create inbox/outbox if not already exists

    if args.mode == 'push_ts':
        copy_serge_and_localize()  # TODO: Call as two separate functions instead?
    else:
        copy_outbox_to_serge()


if __name__ == "__main__":
    main()
