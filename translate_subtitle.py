from deep_translator import GoogleTranslator
from tqdm import tqdm
import os
import sys


def validate_line_format(parts: list[str]) -> bool:
    return len(parts) == 3 and \
        parts[0].isdigit() and \
        len(parts[1].split(" --> ")) == 2


def translate_line(line: str) -> str:
    parts = line.split("\n", 2)

    if not validate_line_format(parts):
        print(f'Malformed subtitle in line: {line}')
        return line

    text = parts[2]
    parts[2] = GoogleTranslator(
        source='en', target='es').translate(text.strip()) or text

    return "\n".join(parts)


def translate_file(lines: list[str]) -> list[str]:
    translated_lines = map(
        lambda line: translate_line(line) + '\n',
        tqdm(lines, unit='line', total=len(lines), leave=True)
    )

    return list(translated_lines)


def read_and_parse_file(file_path: str) -> list[str]:
    lines = []
    tmp = ""

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip().isdigit():
                tmp += line
                continue
            if tmp:
                lines.append(tmp.strip())
            tmp = line

        if tmp:
            lines.append(tmp.strip())

    return lines


def write_translated_file(file_path: str, lines: list[str]) -> None:
    translated_file_path = os.path.splitext(file_path)[0] + '_es.srt'

    with open(translated_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(f'Usage: python3 {sys.argv[0]} /path/to/file.srt')
        sys.exit(1)

    file_path = sys.argv[1]

    if not file_path.endswith('.srt'):
        print(f'{file_path} must be a subtitle file .srt')
        sys.exit(1)

    lines = read_and_parse_file(file_path)
    translated_lines = translate_file(lines)
    write_translated_file(file_path, translated_lines)
