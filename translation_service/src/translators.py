# Base class for a membership check
import sys
from abc import ABCMeta, abstractmethod
from google.cloud import translate_v2

# Cache the translators created to avoid reinitializing
CACHED_TRANSLATORS = {}

SUPPORTED_TRANSLATION_APIS = {"google", "caps"}


class Translator:
    __metaclass__ = ABCMeta

    # Register an item as being a member
    @abstractmethod
    def translate(self, texts_list, target_lang_iso): raise NotImplementedError


class CapsTranslator(Translator):
    """Translator that capitalizes text."""

    def translate(self, texts_list, target_lang_iso):
        """Capitalizes the text.

            Args:
                texts_list: A list of untranslated strings.
                target_lang_iso: Target language ISO-639-1 identifier (ex. "es").

            Returns:
                A list of the capitalized strings.
        """

        return [text.upper() for text in texts_list]


class GoogleTranslator(Translator):
    """Translator that uses the Google Cloud Translation API to translate text.

        Attributes:
            google_client: The Google Cloud Translation Client which can be called to translate text.
    """

    def __init__(self, google_key_path):
        """Constructor that initializes the Google Cloud Translation Client.

            Args:
                google_key_path: The path to the JSON file for the Google Services keyfile.
        """
        self.google_client = translate_v2.Client.from_service_account_json(google_key_path)

    def translate(self, texts_list, target_lang_iso):
        """Calls Google Translate API to translate text to given language.

            Args:
                texts_list: A list of untranslated strings.
                target_lang_iso: The target language (ISO-639-1 identifier) for localization.

            Returns:
                A list of localized/translated strings.
        """

        # Send list of texts to Google Translate
        translation_list = self.google_client.translate(texts_list, target_language=target_lang_iso)

        # Grab the translated texts from the list of dictionaries returned by Google
        localized_texts = [translation.get('translatedText') for translation in translation_list]

        return localized_texts


class TranslatorFactory:

    @staticmethod
    def get_translator(translation_api="caps", google_key_path=None):
        """Gets the appropriate Translator from CACHED_TRANSLATORS, or creates a new one if needed.

        Args:
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile.

        Returns:
            The Translator object based on the translation_api argument.

        """

        # Validate the arguments for building a Translator
        validate_translator_args(translation_api, google_key_path)

        if translation_api not in CACHED_TRANSLATORS:
            if translation_api == "google":
                CACHED_TRANSLATORS[translation_api] = GoogleTranslator(google_key_path)
            else:
                # Default is to capitalize the text
                CACHED_TRANSLATORS[translation_api] = CapsTranslator()
        return CACHED_TRANSLATORS[translation_api]


def validate_translator_args(translation_api, google_key_path):
    """Validates the arguments for creating a Translator. Exits with message if any invalid args.

        Args:
            translation_api: Translation API to use ("google" for Google Translate,
                            "caps" for capitalization (default)).
            google_key_path: Path for the Google Service Account JSON keyfile.
    """

    # Check that the translation API is supported
    if translation_api not in SUPPORTED_TRANSLATION_APIS:
        sys.exit("ERROR: Translation API is not supported. Supported APIs include: {}.".format(
            SUPPORTED_TRANSLATION_APIS))

    if translation_api == "google" and google_key_path is None:
        sys.exit("ERROR: To use the Google Translate API, you must include the google_key_path.")
