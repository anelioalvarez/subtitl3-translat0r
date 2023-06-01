from subtitle import Subtitle
from tqdm import tqdm
import optparse
from translation_helper import is_language_supported, text_partition, translate_partition
from constants import *
import os
import sys
import re


def translate_subtitles(subtitles: list[Subtitle], source: str, target: str) -> list[Subtitle]:
    subtitle_texts = [subtitle.text for subtitle in subtitles]
    partitions = text_partition(subtitle_texts)
    translated_texts = []

    try:
        for partition in tqdm(partitions, leave=True):
            translated_texts += translate_partition(partition, source, target)
    except:
        print("Error trying to translate the file")
        sys.exit(1)

    for i in range(len(subtitles)):
        subtitles[i].text = translated_texts[i]

    return subtitles


def read_and_parse_srt(filepath: str) -> list[Subtitle]:
    with open(filepath, 'r', encoding='utf-8') as f:
        file = f.read()

    matches = re.findall(SRT_REGEX_PATTERN, file, re.MULTILINE)
    subtitles = [Subtitle(line_count, start, end, text)
                 for line_count, start, end, text in matches]

    return subtitles


def write_translated_srt(filepath: str, subtitles: list[Subtitle], target: str) -> None:
    translated_filepath = os.path.splitext(filepath)[0] + f'_{target}.srt'

    with open(translated_filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(map(str, subtitles)))


def main():
    parser = optparse.OptionParser(
        usage="usage: %prog [options] path/to/file.srt")

    parser.add_option("-s", "--source",
                      default=DEFAULT_TRANSLATION_SOURCE,
                      help='source language for translation. [default: %default]')
    parser.add_option("-t", "--target",
                      default=DEFAULT_TRANSLATION_TARGET,
                      help='target language for translation. [default: %default]')

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    filepath = args[0]
    source = options.source
    target = options.target

    if not os.path.isfile(filepath) or not filepath.endswith('.srt'):
        print(f'"{filepath}" must be a srt file.')
        sys.exit(1)

    if not is_language_supported(source, target):
        print('Languages not supported.')
        sys.exit(1)

    subtitles = read_and_parse_srt(filepath)
    translated_subtitles = translate_subtitles(subtitles, source, target)
    write_translated_srt(filepath, translated_subtitles, target)


if __name__ == '__main__':
    main()
