SRT_REGEX_PATTERN = r"^\s*([0-9]+)[\n]+(\d+:\d+:\d+,\d+)[^\S\n]+-->[^\S\n]+(\d+:\d+:\d+,\d+)((?:\n(?!\d+:\d+:\d+,\d+\b|\n+\d+$).*)*)"


class Subtitle:

    def __init__(self, line_count: int, start: str, end: str, text: str):
        self._line_count = line_count
        self._start = start
        self._end = end
        self._text = text.strip().replace('\n', ' ')

    @property
    def line_count(self) -> int:
        return self._line_count

    @property
    def start(self) -> str:
        return self._start

    @property
    def end(self) -> str:
        return self._end

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text.strip().replace('\n', ' ')

    def __str__(self) -> str:
        return f"{self._line_count}\n{self._start} --> {self._end}\n{self._text}"

    def __repr__(self) -> str:
        return f"{self._line_count}\n{self._start} --> {self._end}\n{self._text}"
