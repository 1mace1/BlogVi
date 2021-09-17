from pathlib import Path
from typing import Optional

import yaml

from ._config import SETTINGS_DEFAULTS, SETTINGS_FILENAME


class SettingsError(Exception):
    """Base class for settings errors."""


class SettingsFileNotFoundError(SettingsError):
    """Raised when settings file not found."""

    default_message = ('Could not file settings file.'
                       ' Please, make sure, that the settings file does exist in the working directory'
                       f' and called `{SETTINGS_FILENAME}`')

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.default_message

        super().__init__(self.message)


class MandatorySettingNotFoundError(SettingsError):
    """Raised when a mandatory settings not found in the settings file."""

    default_message = ('Missing mandatory setting: {name}.'
                       f' Please provide it in your `{SETTINGS_FILENAME}`.')

    def __init__(self, name: str, message: Optional[str] = None):
        self.name = name
        self.message = message or self.get_default_message()

        super().__init__(self.message)

    def get_default_message(self):
        return self.default_message.format(name=self.name)


class Settings:
    mandatory = ('blog_name', 'blog_root_url', 'blog_post_location_url', 'domain_url')
    optional = SETTINGS_DEFAULTS

    def __init__(self, workdir: Path, templates_dir: Path, **settings):
        self.workdir = workdir
        self.templates_dir = templates_dir

        self.fill_settings(settings)

    def fill_settings(self, settings):
        # Fill mandatory settings.
        # Raises `MandatorySettingNotFoundError`, when one ore more mandatory settings not found.
        for mandatory in self.mandatory:
            try:
                self.__dict__.update({mandatory: settings[mandatory]})
            except KeyError:
                raise MandatorySettingNotFoundError(mandatory)

        # Fill optional settings.
        for optional_name, optional_default in self.optional.items():
            self.__dict__.update({optional_name: settings.get(optional_name, optional_default)})

        # Fill other settings if they exist
        for key, value in settings.items():
            try:
                self.__dict__.update({key: settings[key]})
            except KeyError:
                pass


def get_settings(filename: str = SETTINGS_FILENAME) -> dict:
    """Return settings dictionary.

    :param filename: path to yaml settings file, defaults to `1_settings.yaml`
    :return: settings dictionary object
    :rtype: dict
    """

    try:
        with open(filename) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        raise SettingsFileNotFoundError
