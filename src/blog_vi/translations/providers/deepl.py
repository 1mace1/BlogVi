from .base import BaseTranslateProvider
import deepl


class DeeplTranslateProvider(BaseTranslateProvider):
    id = 'deepl'
    settings_key = 'deepl_translator'

    def translate(self, text: str, source_abbreviation: str, target_abbreviation: str) -> str:
        api_key = getattr(self, '_BaseTranslateProvider__api_key')
        translator = deepl.Translator(auth_key=api_key)
        result = translator.translate_text(text, source_lang=source_abbreviation, target_lang=target_abbreviation)
        return result.text
