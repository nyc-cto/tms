import unittest
import sys
sys.path.append('src')
import translators

GOLDEN_PO_MSGSTR_TEXTS = ["", "Let's get things translated!",
                          "We can use machine translation to get many localizations done automatically and quickly."]

# Golden version is the capitalized version since CapsTranslator is default
GOLDEN_LOCALIZED_TEXTS = ["", "LET'S GET THINGS TRANSLATED!",
                          "WE CAN USE MACHINE TRANSLATION TO GET MANY LOCALIZATIONS DONE AUTOMATICALLY AND QUICKLY."]

TARGET_LANG_ISO = 'es'


class TestTranslators(unittest.TestCase):

    def test_translate(self):
        """
        Translator.translate
            expected in: texts_list (golden), target_lang_iso
            expected out: localized_texts
        """

        # Call get_translator method to get the default translator (CapsTranslator)
        translator = translators.TranslatorFactory.get_translator()

        # Call the translate method using the golden input
        localized_texts = translator.translate(GOLDEN_PO_MSGSTR_TEXTS, TARGET_LANG_ISO)

        # TEST: Compare the output with the golden output
        self.assertEqual(localized_texts, GOLDEN_LOCALIZED_TEXTS)

    def test_translatorfactory_get_translator_default(self):
        """
        TranslatorFactory.get_translator
            expected in: None
            expected out: a CapsTranslator (default type)
        """

        # Call get_translator method to get the default translator
        default_translator = translators.TranslatorFactory.get_translator()

        # TEST: Ensure the default translator is a CapsTranslator
        self.assertIsInstance(default_translator, translators.CapsTranslator)


if __name__ == '__main__':
    unittest.main()
