from .base import BaseTranslateProvider
import deepl


class DeeplTranslateProvider(BaseTranslateProvider):
    id = 'deepl'

    def translate(self, text: str, source_abbreviation: str, target_abbreviation: str) -> str:
        translator = deepl.Translator(auth_key='0dabe962-0c67-684f-2122-4caaed052039')
        result = translator.translate_text(text, source_lang=source_abbreviation, target_lang=target_abbreviation)
        return result.text
