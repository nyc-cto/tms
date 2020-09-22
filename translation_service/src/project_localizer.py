from po_file import PoFile
from translators import TranslatorFactory
import argparse
import os
import sys

# TODO: Update with complete list of languages; possibly in a separate file (currently only NYC required languages)
# Target language ISO-639-1 identifier (ex. "es")
SUPPORTED_LANGUAGES = {'es', 'zh', 'ru', 'bn', 'ht', 'ko', 'ar', 'fr', 'ur', 'pl'}


def localize_project(input_dir, output_dir, translation_api='caps', google_key_path=None):
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
            google_key_path: Path for the Google Service Account JSON keyfile (not required if not using this API).
    """

    #  Create a translator object based on the translation_api
    translator = TranslatorFactory.get_translator(translation_api, google_key_path)

    # Get a list of all the target language subdir names for this project
    # NOTE: will skip any subdir that is not a supported target language ISO code
    # TODO: Add in warning for any non-supported languages (print to stdout? Other?)
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


def localize_po_file(in_dir, out_dir, po_file, target_lang_iso, translator):
    """Creates a localized version of hte po_file

        Args:
            in_dir: The filepath for the directory with the .po files.
            out_dir: The filepath to write the localized .po files to.
            po_file: The filename of the .po file to localize.
            target_lang_iso: The target language (ISO-639-1 identifier) for localization.
            translator: The Translator object to use to translate texts.
    """
    # Create output file name based on po_file and language code
    po_filepath = os.path.join(in_dir, po_file)
    localized_po_filepath = os.path.join(out_dir, po_file)

    # Create a PoFile object
    po = PoFile(po_filepath)

    # Parse the po file
    po.parse_po_file()

    # Translate the po file
    po.translate_po_file(target_lang_iso, translator)

    # Write the localized/translated .po file
    po.write_localized_po_file(localized_po_filepath)


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
