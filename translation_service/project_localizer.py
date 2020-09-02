from po_localizer import localize_po_file
from translators import TranslatorFactory
import argparse
import os
import sys

# TODO: Update with complete list of languages; possibly in a separate file (currently only NYC required languages)
# Target language ISO-639-1 identifier (ex. "es")
SUPPORTED_LANGUAGES = {'es', 'zh', 'ru', 'bn', 'ht', 'ko', 'ar', 'fr', 'ur', 'pl'}
SUPPORTED_TRANSLATION_APIS = {"google", "caps"}


def localize_project(input_dir, output_dir, translation_api, google_key_path):
    """Finds all target language subdirectories in the input project directory and their nested .po files,
        and creates these subdirectories in the output project directory where it writes the localized
        .po files in the target language using the translation API.
        NOTE: Expects to have subdirectories as the next tree level named as the target language ISO-639-1
        identifiers, with .po files to localize in each subdir (ex. input_dir/es/needs_localization.po).

        Args:
            input_dir: Filepath for the input project directory.
            output_dir: Filepath for the output project directory.
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile.
    """

    #  Create a translator object based on the translation_api
    translator = TranslatorFactory.get_translator(translation_api, google_key_path)

    # Get a list of all the target language subdir names for this project
    # NOTE: will skip any subdir that is not a supported target language ISO code
    target_lang_subdirs = [subdir for subdir in os.listdir(input_dir)
                           if os.path.isdir(os.path.join(input_dir, subdir)) and subdir in SUPPORTED_LANGUAGES]

    # Create all localization subdirs in output_dir
    # and write a localized version of each file based on the subdir language
    for target_lang_iso in target_lang_subdirs:

        input_target_lang_subdir = os.path.join(input_dir, target_lang_iso)

        # Get a list of all .po files in this target language subdir
        po_files = [file for file in os.listdir(input_target_lang_subdir) if file.endswith('.po')]

        # Create output subdir
        output_target_lang_subdir = create_output_localized_subdir(output_dir, target_lang_iso)

        # Localize each file in the subdir and write to the output subdir
        for po_file in po_files:

            localize_po_file(input_target_lang_subdir, output_target_lang_subdir,
                                          po_file, target_lang_iso, translator)


def create_output_localized_subdir(output_dir, target_lang_iso):
    """Creates a subdirectory in the output project for the target language.

        Args:
            output_dir: The path to the output project directory.
            target_lang_iso: The target language ISO code, which will also be the subdir name.

        Returns:
            The path for the new target language subdirectory in the output project.

    """

    output_target_lang_subdir = os.path.join(output_dir, target_lang_iso)
    if not os.path.exists(output_target_lang_subdir):
        os.makedirs(output_target_lang_subdir)

    return output_target_lang_subdir


def validate_args(input_dir, output_dir, translation_api, google_key_path):
    """Validates the arguments for this program. Exits with message if any invalid args.

        Args:
            input_dir: Filepath for the input file.
            output_dir: Filepath for the output directory.
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile.
    """

    # Check input file directory
    if not os.path.isdir(input_dir):
        sys.exit("ERROR: Input directory does not exist.")

    # Check output file directory
    if not os.path.isdir(output_dir):
        sys.exit("ERROR: Output directory does not exist.")

    # Check that the translation API is supported
    if translation_api not in SUPPORTED_TRANSLATION_APIS:
        sys.exit("ERROR: Translation API is not supported. Supported APIs include: {}.".format(
            SUPPORTED_TRANSLATION_APIS))

    if translation_api == "google" and google_key_path is None:
        sys.exit("ERROR: To use the Google Translate API, you must include the google_key_path.")


def main():
    """Localizes all .po files from an input project directory into an output project directory."""
    parser = argparse.ArgumentParser(description='Localizes all .po files in a directory')
    parser.add_argument("--input_dir", help="filepath for input project directory", required=True)
    parser.add_argument("--output_dir", help="filepath for output project directory", required=True)
    parser.add_argument('--translation_api', type=str,
                        help='translation API to use ("google" for Google Translate,'
                             ' "caps" for capitalization)', required=True)
    parser.add_argument('--google_key_path', type=str,
                        help='path for the Google Service Account JSON keyfile', required=False)

    args = parser.parse_args()

    # Validate that all arguments are correct before running program
    validate_args(args.input_dir, args.output_dir, args.translation_api, args.google_key_path)

    # Normalize paths
    args.input_dir, args.output_dir = os.path.normpath(args.input_dir), os.path.normpath(args.output_dir)

    # Localize the project and its po files
    localize_project(args.input_dir, args.output_dir, args.translation_api, args.google_key_path)


if __name__ == "__main__":
    main()
