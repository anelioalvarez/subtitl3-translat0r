from subtitle import Subtitle, SRT_REGEX_PATTERN
from deep_translator import GoogleTranslator
import os
import sys
import re


def is_language_supported(source='en', target='es') -> bool:
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    langs = set(langs_dict.keys()).union(set(langs_dict.values()))

    return {source, target}.issubset(langs)


def translate_subtitles(subtitles: list[Subtitle], source='en', target='es') -> list[Subtitle]:
    all_texts = list(map(lambda subtitle: subtitle.text, subtitles))

    try:
        translated_texts = GoogleTranslator(
            source, target).translate_batch(all_texts)
    except:
        print("Error trying to translate the file")
        sys.exit(1)

    for i in range(len(subtitles)):
        subtitles[i].text = translated_texts[i]

    return subtitles


def read_and_parse_file(filepath: str) -> list[Subtitle]:
    with open(filepath, 'r', encoding='utf-8') as f:
        file = f.read()

    matches = re.findall(SRT_REGEX_PATTERN, file, re.MULTILINE)
    subtitles = []

    for [line_count, start, end, text] in matches:
        subtitles.append(Subtitle(line_count, start, end, text))

    return subtitles


def write_translated_file(filepath: str, subtitles: list[Subtitle], target='es') -> None:
    translated_filepath = os.path.splitext(filepath)[0] + f'_{target}.srt'

    with open(translated_filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(map(str, subtitles)))


def main():
    if len(sys.argv) < 2:
        print(f'Usage: python3 {sys.argv[0]} path/to/file.srt')
        sys.exit(1)

    filepath = sys.argv[1]

    if not filepath.endswith('.srt') or not os.path.isfile(filepath):
        print(f'"{filepath}" must be a srt file.')
        sys.exit(1)

    if not is_language_supported():
        print('Languages not supported.')
        sys.exit(1)

    subtitles = read_and_parse_file(filepath)
    translated_subtitles = translate_subtitles(subtitles)
    write_translated_file(filepath, translated_subtitles)


if __name__ == '__main__':
    main()
