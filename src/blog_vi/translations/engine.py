from copy import copy

from .exceptions import TranslateEngineNotFound
from .registry import translation_provider_registry
from blog_vi.__main__ import Landing, Article


class TranslateEngine:
    def __init__(self, landing: Landing, source_abbreviation: str):
        self.landing = landing
        self.source_abbreviation = source_abbreviation

        self.settings = landing.settings

        self.translator = self.settings.translator

        if not self.translator:
            raise TranslateEngineNotFound(f'{self.translator} not found')

    def translate(self) -> None:
        """Translate landing and its articles into specified in the settings languages."""
        for target_abbreviation in self.settings.translate_list:
            translated_landing = self.translate_landing(target_abbreviation)
            translated_landing.generate()

    def translate_landing(self, target_abbreviation: str) -> Landing:
        """
        Translate landing and its articles into the target language,
        specified by `target_abbreviation` param.
        """
        translated_landing = self.clone_landing_for_translation(target_abbreviation)

        for article in self.landing._articles:
            translated_landing.add_article(self.translate_article(article, target_abbreviation))

        return translated_landing

    def translate_article(self, article: Article, target_abbreviation: str) -> Article:
        """
        Translate article title, summary and text into the target language,
        specified by `target_abbreviation` param.
        """

        translator_cls = translation_provider_registry.get_provider(self.translator)
        translator = translator_cls(api_key='')
        cloned_article = copy(article)

        cloned_article.title = translator.translate(
            text=cloned_article.title,
            source_abbreviation=self.source_abbreviation,
            target_abbreviation=target_abbreviation
        )

        cloned_article.summary = translator.translate(
            text=cloned_article.summary,
            source_abbreviation=self.source_abbreviation,
            target_abbreviation=target_abbreviation
        )

        cloned_article.markdown = translator.translate(
            text=cloned_article.markdown,
            source_abbreviation=self.source_abbreviation,
            target_abbreviation=target_abbreviation
        )

        return cloned_article

    def clone_landing_for_translation(self, folder_name: str) -> Landing:
        workdir = self.landing.workdir / folder_name

        return Landing(
            self.settings,
            self.landing.name,
            link_menu=self.landing.link_menu,
            search_config=self.landing.search_config,
            workdir=workdir
        )
