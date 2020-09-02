# Base class for a membership check
from abc import ABCMeta, abstractmethod
from google.cloud import translate_v2

# Cache the translators created to avoid reinitializing
CACHED_TRANSLATORS = {}


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

        capitalized_texts = []
        for text in texts_list:
            capitalized_texts.append(text.upper())

        return capitalized_texts


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
    def get_translator(translation_api, google_key_path=None):
        if translation_api not in CACHED_TRANSLATORS:
            if translation_api == "google":
                CACHED_TRANSLATORS[translation_api] = GoogleTranslator(google_key_path)
            else:
                # Default is to capitalize the text  # TODO: Change to proper default later
                CACHED_TRANSLATORS[translation_api] = CapsTranslator()
        return CACHED_TRANSLATORS[translation_api]

