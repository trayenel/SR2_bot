import validators
import gettext
import argparse
import tldextract
import babel
from pathlib import Path

def validateUrl(url):
    if validators.domain(url) or validators.url(url):
        return True
    return False


def extractUrl(url):
    return tldextract.extract(url).registered_domain


def init_argparse() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        usage="%(prog)s -c [FILE]",
        description="Start telegram bot.",
    )
    parser.add_argument("file")
    parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="load configuration file",
        required=True,
    )
    return parser

def get_rows(buttons, items_per_row):
    """
    get_rows splits the buttons list into
    smaller ones based on the amount items you
    want per row.

    :param buttons: List of InlineKeyboardButton
    :param items_per_row: Int
    :return: List of List of InlineKeyboardButton
    """
    result = []
    tmp = []
    for index, button in enumerate(buttons):
        tmp.append(buttons[index])
        if (index + 1) % items_per_row == 0:
            result.append(tmp)
            tmp = []

    if len(tmp) > 0:
        result.append(tmp)

    return result

def setup_gettext():
    """
    Setups gettext text domains.
    """
    gettext.bindtextdomain('SR2_bot', './locales')
    gettext.textdomain('SR2_bot')

def setLanguage(language):
    gettext.translation(
        "SR2_bot", "./locales", fallback=True, languages=[language.strip()]
    ).install()

def _get_available_langs():
    """
    Gets all available/translated languages by searching against babel's list.
    """
    langs = ['en', 'ro', 'fa']
    languages = [*babel.Locale("en").languages, "zh-CN", "zh-TW"]

    for locale in gettext.find('SR2_bot', './locales', languages=languages, all=True):
        parts = Path(locale).relative_to('/locales').parts
        # Assume there are at least 2 parts
        if len(parts) >= 2:
            langs.append(str(parts[0]))

    return langs

def _get_full_names():
    """
    Gets a dictionary of {locale: { full_name, translation }}, where full_name is the
    name of the language in it's own language (eg. el_GR => Ελληνικά) and translation
    is the gettext translation (with fallback).
    """
    full_length_names = {}
    for locale in _get_available_langs():
        babel_locale = locale

        if locale == "zh-CN":
            babel_locale = "zh_hans"
        elif locale == "zh-TW":
            babel_locale = "zh_hant"

        full_length_names[locale.lower()] = {
            "full_name": babel.Locale.parse(babel_locale).get_display_name(
                babel_locale
            ),
            "translation": gettext.translation(
                'SR2_bot', './locales', languages=[locale], fallback=True
            ),
        }
    return full_length_names


# This exists so the above two - expensive - functions, only run once on startup.
available_locales = _get_full_names()

def get_translation(locale="en"):
    """
    Gets the gettext#translation of the locale.
    """
    lang = locale.lower()
    if lang not in available_locales.keys():
        # If language is not translated, let gettext handle it.
        # Usually on start command & custom queries.
        return gettext.translation(
            'SR2_bot', './locales', languages=[locale], fallback=True
        ).gettext
    return available_locales[lang]["translation"].gettext
