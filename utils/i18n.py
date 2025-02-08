from fluent_compiler.bundle import FluentBundle

from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {"ru": ("ru", "en"), "en": ("en", "ru")},
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU", filenames=["locales/ru.ftl"]
                ),
            ),
        ],
    )
    return translator_hub
