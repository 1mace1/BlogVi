from .base import BaseTranslateProvider
from google.cloud import translate_v2 as translate


class GoogleTranslateProvider(BaseTranslateProvider):
    id = 'google'
    settings_key = 'google_translator'

    def __init__(self, api_key: str):
        self.__api_key = api_key

    def translate(self, text: str, source_abbreviation: str, target_abbreviation: str) -> str:
        provider = self.get_provider()
        result = provider.translate(text, target_abbreviation)
        return result["translatedText"]

    def get_provider(self):
        return translate.Client()
