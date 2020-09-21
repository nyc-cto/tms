PO_LINE_LEN = 80  # Max line length .po files prefer for printing on first line of msgstr


class MsgElement:
    """Class for a message element from a .po file

        Attributes:
            msgheader: A list of header lines for the msg element.
            msgid: A list of msgid lines for the msg element (text lines to be translated).
            msgstr: A list of msgstr lines for the msg element (translated versions of the text lines).
            msgstr_translated: A boolean. True if the msgstr is translated. False otherwise.
    """

    def __init__(self, msgheader, msgid, msgstr, msgstr_translated=False):
        """Constructor for a MsgElements object.

            Args:
                msgheader: A list of header lines for the msg element.
                msgid: A list of msgid text for the msg element (text lines to be translated).
                msgstr: A list of msgstr text for the msg element (translated versions of the text).
                msgstr_translated: A boolean. True if the msgstr is translated. False otherwise.
        """
        self.msgheader = msgheader
        self.msgid = msgid
        self.msgstr = msgstr
        self.msgstr_translated = msgstr_translated

    def get_msgid_text(self):
        """Returns a single concatenated string version of the text in the msgid list."""

        msgid_text = ""

        for line in self.msgid:

            # Remove "msgid" from the line if present
            if line.startswith("msgid"):
                line = line[len("msgid "):].strip()

            # Remove quotes at the beginning/ending of the line
            # and add to the msgid_text
            msgid_text += line.strip('"')

        return msgid_text

    def add_msgstr_translation(self, translation_list):
        """Adds a translated version of a msgstr, replacing the previous version.

            Args:
                translation_list: A list of strings with the msgstr translation to add.
        """
        # Add the translation to the msgstr with the surrounding "msgstr"
        # and quotes as required in a po file
        if len(translation_list) == 1 and len('msgstr ""') + len(translation_list) < PO_LINE_LEN:
            # Single translation string that is small enough to keep on a single line
            self.msgstr = ['msgstr "' + translation_list[0] + '"']
        else:
            # Longer or multiple translation strings, put into multiple lines
            self.msgstr = ['msgstr ""']
            for translation in translation_list:
                self.msgstr.append('"' + translation + '"')

        # Set this element's msgstr_translated to True
        self.msgstr_translated = True


class PoFile:
    """Class to hold information about .po file elements.

        Attributes:
            po_filepath: The filepath for the .po file to parse.
            header: A list of header lines from the .po file
            msg_elements: A list of msg elements from the .po file.
    """

    def __init__(self, po_filepath):
        """Constructor for a PoFile object.

            Args:
                po_filepath: The filepath for the .po file to parse.
        """
        self.po_filepath = po_filepath
        self.header = []
        self.msg_elements = []

    def parse_po_file(self):
        """Parses the .po file to find the header and each message element (which contains
        a message header, a msgid (untranslated string), and a msgstr (translated version of the msgid).
        See https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html
        for detail on the structure of a .po file.
        Assumptions about the po file:
            - File starts with a header.
            - A single blank line proceeds each message element.
            - Each message element has a message header, msgid, and msgstr.
        """

        with open(self.po_filepath) as f:

            # Flags to track which part of the file we are in
            processing_header = True  # Always start with a header in a po file
            processing_msg_header = False
            processing_msgid = False
            processing_msgstr = False
            msgstr_empty = True

            # Lists to keep track of current element lines
            elem_header = []
            elem_msgid = []
            elem_msgstr = []

            for line in f:

                # Remove any extra whitespace from the line
                clean_line = line.strip()

                # Determine if handling the po file header or one of the msg elements
                if processing_header:
                    # Until hitting a blank line, all the beginning lines are part of the po file header
                    if len(clean_line) != 0:
                        self.header.append(clean_line)  # Add line to the header
                    else:
                        processing_header = False  # Done with the header
                        processing_msg_header = True  # Next will process a msg header
                else:

                    # Determine if in the middle of processing an element or starting a new one
                    if len(clean_line) == 0:
                        # Blank line means the element is done being processed

                        # Create a MsgElement object to hold these element lines
                        if msgstr_empty:
                            # An empty msgstr means that it has not been translated
                            elem = MsgElement(elem_header, elem_msgid, elem_msgstr, msgstr_translated=False)
                        else:
                            elem = MsgElement(elem_header, elem_msgid, elem_msgstr, msgstr_translated=True)

                        # Add this element to the PoFile.msg_elements
                        self.msg_elements.append(elem)

                        # Reset the flags for a new element
                        processing_msg_header = True
                        processing_msgid = False
                        processing_msgstr = False
                        msgstr_empty = True

                        # Reset the lists to keep track of current element lines
                        elem_header = []
                        elem_msgid = []
                        elem_msgstr = []

                    else:
                        # In the middle of processing an element

                        # Find where the msgid starts (which also ends the msg_header)
                        if clean_line.startswith("msgid"):
                            processing_msg_header = False
                            processing_msgid = True

                        # Find where the msgstr starts (which also ends the msgid)
                        if clean_line.startswith("msgstr"):
                            processing_msgid = False
                            processing_msgstr = True

                        # Handle current part of the msg element
                        if processing_msg_header:
                            elem_header.append(clean_line)
                        elif processing_msgid:
                            elem_msgid.append(clean_line)
                        else:
                            # Processing msgstr
                            elem_msgstr.append(clean_line)

                            # If the msgstr isn't empty, switch msgstr_empty to False
                            if clean_line.startswith("msgstr") and clean_line != 'msgstr ""':
                                # If there is anything inside of the msgstr, it's not empty
                                # (ex. 'msgstr "Hello"')
                                msgstr_empty = False
                            if clean_line.startswith('"'):
                                # If there are any lines in quotes after the msgstr starts, it's not empty
                                # (ex. '"Hello"')
                                msgstr_empty = False

            # Handle last element at the end of file if it wasn't completed (due to lack of extra blank line)
            if processing_msgstr:
                # Create a MsgElement object to hold these element lines
                if msgstr_empty:
                    # An empty msgstr means that it has not been translated
                    elem = MsgElement(elem_header, elem_msgid, elem_msgstr, msgstr_translated=False)
                else:
                    elem = MsgElement(elem_header, elem_msgid, elem_msgstr, msgstr_translated=True)

                # Add this element to the PoFile.msg_elements
                self.msg_elements.append(elem)

    def translate_po_file(self, target_lang_iso, translator):
        """For a PoFile object, adds translated msgstrs to any msg_element that is untranslated
            using the specified translator and target language.

            Args:
                target_lang_iso: The target language (ISO-639-1 identifier) for localization.
                translator: The Translator object to use to translate texts.
        """

        for elem in self.msg_elements:
            if not elem.msgstr_translated:
                # Only translate the untranslated msgstrs
                translation_list = translator.translate([elem.get_msgid_text()], target_lang_iso)
                elem.add_msgstr_translation(translation_list)

    def write_localized_po_file(self, localized_po_filepath):
        """Writes a localized version of a .po file to the specified path.

            Args:
                localized_po_filepath: The filepath to write the localized .po to.
        """

        # Write file using unix-style line endings
        with open(localized_po_filepath, 'w', newline='') as wf:

            # Write the header first
            for line in self.header:
                wf.write(line + "\n")

            # Write each element
            for elem in self.msg_elements:

                # Add a blank line before each element
                wf.write("\n")

                # Write out the header, msgid, and msgstr lists

                for line in elem.msgheader:
                    wf.write(line + "\n")

                for line in elem.msgid:
                    wf.write(line + "\n")

                for line in elem.msgstr:
                    wf.write(line + "\n")
