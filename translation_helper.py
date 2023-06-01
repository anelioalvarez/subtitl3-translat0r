from deep_translator import GoogleTranslator
from constants import *


def is_language_supported(source: str, target: str) -> bool:
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    langs = set(langs_dict.keys()).union(set(langs_dict.values()))

    return {source, target}.issubset(langs)


def text_partition(texts: list[str], max_chars=MAX_CHARS_GOOGLE_TRANSLATOR) -> list[list[str]]:
    partitions = []
    current_partition = []
    current_length = 0
    limit = max_chars - len(texts) + 1

    for text in texts:
        text_length = len(text)

        if current_length + text_length <= limit:
            current_partition.append(text)
            current_length += text_length
        else:
            partitions.append(current_partition)
            current_partition = [text]
            current_length = text_length

    if current_partition:
        partitions.append(current_partition)

    return partitions


def translate_partition(partition: list[str], source: str, target: str) -> list[str]:
    translation = GoogleTranslator(
        source, target).translate('\n'.join(partition))
    return translation.split('\n')
