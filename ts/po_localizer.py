import argparse
import os

PO_LINE_LEN = 80
LOCALIZED_DIR = "localized"


def localize_all_po_files(in_path, out_path, lang):
    """Finds all .po files in a directory and localizes them in the given language.

        Args:
            in_path: The filepath for the directory with the .po files
            out_path: (optional) The filepath to write the localized .po files to
            lang: The target language (ISO-639-1 identifier) for localization
    """
    # TODO: Decide where to store & naming format for localized files

    # Create directory for localized files to be placed in if not provided
    if out_path is None:
        out_path = os.path.join(in_path, LOCALIZED_DIR)
        if not os.path.exists(out_path):
            os.makedirs(out_path)

    for f in os.listdir(in_path):
        if f.endswith('.po'):
            localize_po_file(in_path, out_path, f, lang)


def localize_po_file(in_path, out_path, po_file, lang):
    """Parses the given po file to find all msgid(untranslated string)
        and add lang translation in corresponding msgstr(translated string)

        Args:
            in_path: The filepath for the directory with the .po files
            out_path: The filepath to write the localized .po files to
            po_file: The filename of the .po file to localize
            lang: The target language (ISO-639-1 identifier) for localization
    """
    # Create output file name based on po_file and language code
    localized_po_file = po_file[:-len('.po')] + "_" + lang + '.po'
    po_filepath = os.path.join(in_path, po_file)
    localized_po_filepath = os.path.join(out_path, localized_po_file)

    # Write to localized po file as we read the original po file and translate
    with open(localized_po_filepath, 'w') as wf:

        with open(po_filepath) as rf:
            msgid_started = False
            msgstr_started = False

            text = ""
            for line in rf:
                clean_line = line.strip()  # remove any extra whitespace

                # Find where the msgid starts
                if clean_line.startswith("msgid"):
                    msgid_started = True
                    clean_line = clean_line[len("msgid "):].strip()

                # When starting msgstr, ending msgid
                if clean_line.startswith("msgstr"):
                    msgid_started = False
                    msgstr_started = True

                # Add any parts of msgid to the text
                if msgid_started:
                    text += clean_line.strip('"')
                    # TODO: Currently creates a single long string for translation,
                    # but perhaps this should be separated as in the original?
                    # Note that separation would cause issues with the translation quality.

                # Write all lines to localized file
                if msgstr_started:
                    # Get and write the translation

                    loc_text = translate_text(text, lang)

                    if len('msgstr ""') + len(loc_text) < 80:
                        # Small enough to write on a single line
                        wf.write('msgstr "' + loc_text + '"\n')
                    else:
                        # Write on multiple lines
                        wf.write(line)
                        wf.write('"' + loc_text + '"\n')
                    text = ""  # reset text
                    msgstr_started = False
                else:
                    # Write original line
                    wf.write(line)


def translate_text(text, lang):
    """Translates string to the given language.

        Args:
            text: An untranslated string
            lang: The target language (ISO-639-1 identifier) for localization

        Returns:
            The localized string
    """
    # Don't translate empty strings, just return an empty string
    if text == "":
        return ""

    # TODO: call Google Translate or other translation service; for now, uppercase placeholder
    return text.upper()


def main():
    """Localizes all .po files in a directory"""
    # TODO: Write a wrapper for all of ts file structure that auto-grabs ISO lang codes
    parser = argparse.ArgumentParser(description='Localizes all .po files in a directory')
    parser.add_argument("--input", help="filepath for input directory", required=True)
    parser.add_argument("--output", help="filepath for output directory", required=False)
    parser.add_argument('--lang', type=str,
                        help='target language ISO-639-1 identifier (ex. "es")', required=True)
    args = parser.parse_args()
    localize_all_po_files(args.input, args.output, args.lang)


if __name__ == "__main__":
    main()
