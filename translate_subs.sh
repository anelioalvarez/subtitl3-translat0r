#!/bin/bash

DIR="$1"

if [ ! -d "$DIR" ]; then
    echo "USAGE: $0 /path/to/directory"
    exit 1
fi

declare -i PROCESSED_FILES=0

FILE_COUNTER=$(find "$DIR" -type f -name "*.srt" ! -name "*_es.srt" | wc -l)

find "$DIR" -type f -name "*.srt" ! -name "*_es.srt" | while read FILENAME; do
    echo "PROCESSING FILE [$((PROCESSED_FILES + 1)) of $FILE_COUNTER]:"
    echo \"$(basename "$FILENAME")\"

    python3 translate_subtitle.py "$FILENAME"

    if [ $? -eq 0 ]; then
        echo -e "#OK: the file \"$FILENAME\" has been translated.\n"
    else
        echo -e ">>>>ERROR: the file \"$FILENAME\" could not be translated.\n" >&2
    fi

    ((PROCESSED_FILES++))
done

echo "COMPLETE PROCESS."
