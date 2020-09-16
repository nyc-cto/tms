import os

PO_LINE_LEN = 80  # Max line length .po files prefer for printing on first line of msgstr


def localize_po_file(in_path, out_path, po_file, target_lang_iso, translator):
    """Parses the given .po file to find all msgid(untranslated string)
        and add lang translation in corresponding msgstr(translated string).
        See https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html
        for detail on the structure of a .po file.

        Args:
            in_path: The filepath for the directory with the .po files.
            out_path: The filepath to write the localized .po files to.
            po_file: The filename of the .po file to localize.
            target_lang_iso: The target language (ISO-639-1 identifier) for localization.
            translator: The Translator object to use to translate texts.
    """
    # Create output file name based on po_file and language code
    po_filepath = os.path.join(in_path, po_file)
    localized_po_filepath = os.path.join(out_path, po_file)

    # Parse the .po file
    po_lines, po_msgstr_texts = parse_po_lines(po_filepath)

    # Translate the msgstr lines
    localized_texts = translator.translate(po_msgstr_texts, target_lang_iso)

    # Write the localized/translated .po file
    write_po_localized_file(localized_po_filepath, po_lines, localized_texts)


# TODO: possibly update to handle more complex types of .po files (IF Serge makes them)
#       In particular, msgid_plural/msgstr_plural
#       May want to create a class to handle the data in a more structured way
def parse_po_lines(po_filepath):
    """Parses the .po file to grab each line and find the text to translate.

        Args:
            po_filepath: The filepath for the .po file to parse.

        Returns:
            po_lines: A list of every line as it appears exactly in the .po file.
            po_msgstr_texts: A list of the concatenated texts found in each
                            msgid that need to be translated into the corresponding msgstr.

    """
    po_lines = []  # All original file lines
    po_msgstr_texts = []  # Untranslated texts

    with open(po_filepath) as rf:
        msgid_started = False
        msgstr_started = False
        msgstr_empty = False

        text = ""
        msgstr_text = ""
        for line in rf:

            # Add all lines to the po_lines list
            po_lines.append(line)

            # Process the line for msgid/msgstr by removing any extra whitespace
            clean_line = line.strip()

            # Find where the msgid starts
            if clean_line.startswith("msgid"):
                msgid_started = True
                clean_line = clean_line[len("msgid "):].strip()

            # When starting msgstr, end the msgid
            if clean_line.startswith("msgstr"):
                msgid_started = False
                msgstr_started = True

            # Add any parts of msgid to the text
            if msgid_started:
                text += clean_line.strip('"')
                # TODO: Currently creates a single long string for translation,
                #   but perhaps this should be separated as in the original?
                #   Note that separation would cause issues with the translation quality.

            # Process the msgstr, which may or may not be empty
            if msgstr_started:

                # If there is no message, follow previous method (but wait until done)
                # Need a blank line OR end of file... yeesh.

                # Add the text po_msgstr_texts list to be translated
                po_msgstr_texts.append(text)

                text = ""  # Reset text
                msgstr_started = False

                #


            # # Add all lines to the po_lines list
            # if msgstr_started:
            #
            #     # Add to po_lines
            #     po_lines.append(line)
            #
            #     # Also add the text po_msgstr_texts list to be translated
            #     po_msgstr_texts.append(text)
            #
            #     text = ""  # Reset text
            #     msgstr_started = False
            # else:
            #     # Not a msgstr, so just add to po_lines
            #     po_lines.append(line)

    return po_lines, po_msgstr_texts


def write_po_localized_file(localized_po_filepath, po_lines, localized_texts):
    """Writes a localized version of a .po file.

        Args:
            localized_po_filepath: The filepath to write the localized .po to.
            po_lines: The original lines in the unlocalized .po file.
            localized_texts: The localized msgstr lines only from the .po file.
    """

    current_localized_line = 0

    # Write file using unix-style line endings
    with open(localized_po_filepath, 'w', newline='') as wf:

        for line in po_lines:

            # if line.startswith("msgstr"):
            if line.strip().startswith("msgstr"):
                # Need to use the localized msgstr instead of the original empty one

                if len('msgstr ""') + len(localized_texts[current_localized_line]) < PO_LINE_LEN:
                    # Small enough to write on a single line
                    wf.write('msgstr "' + localized_texts[current_localized_line] + '"\n')
                else:
                    # Write on multiple lines
                    wf.write(line)
                    wf.write('"' + localized_texts[current_localized_line] + '"\n')

                # Increment the localized line
                current_localized_line += 1

            else:
                # Write out the line as-is (not a msgstr translation line)
                wf.write(line)
