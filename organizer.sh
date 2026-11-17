#!/bin/bash

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"
LOG_FILE="organizer.log"

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
fi

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found in the current directory."
    exit 1
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_FILE="grades_${TIMESTAMP}.csv"

mv "$SOURCE_FILE" "${ARCHIVE_DIR}/${ARCHIVED_FILE}"
touch "$SOURCE_FILE"

echo "[${TIMESTAMP}] Original: ${SOURCE_FILE} | Archived: ${ARCHIVE_DIR}/${ARCHIVED_FILE}" >> "$LOG_FILE"
echo "Success: Archived '${SOURCE_FILE}' as '${ARCHIVE_DIR}/${ARCHIVED_FILE}' and reset workspace."
