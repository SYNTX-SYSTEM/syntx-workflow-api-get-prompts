#!/bin/bash
# Monthly Archive Script
LOGS_DIR="/opt/syntx-config/logs"
ARCHIVE_DIR="/opt/syntx-config/logs/archive"
YEAR_MONTH=$(date -d "last month" +%Y%m)

echo "=========================================="
echo "Monthly Archive: $(date)"
echo "=========================================="

mkdir -p "$ARCHIVE_DIR"

FIELD_FILES=$(ls "$LOGS_DIR"/field_flow.$YEAR_MONTH*.jsonl 2>/dev/null)
if [ -n "$FIELD_FILES" ]; then
    cat $FIELD_FILES | gzip > "$ARCHIVE_DIR/field_flow.$YEAR_MONTH.jsonl.gz"
    echo "✅ Archived field_flow"
    rm $FIELD_FILES
fi

WRAPPER_FILES=$(ls "$LOGS_DIR"/wrapper_requests.$YEAR_MONTH*.jsonl 2>/dev/null)
if [ -n "$WRAPPER_FILES" ]; then
    cat $WRAPPER_FILES | gzip > "$ARCHIVE_DIR/wrapper_requests.$YEAR_MONTH.jsonl.gz"
    echo "✅ Archived wrapper_requests"
    rm $WRAPPER_FILES
fi

EVOLUTION_FILES=$(ls "$LOGS_DIR"/evolution.$YEAR_MONTH*.jsonl 2>/dev/null)
if [ -n "$EVOLUTION_FILES" ]; then
    cat $EVOLUTION_FILES | gzip > "$ARCHIVE_DIR/evolution.$YEAR_MONTH.jsonl.gz"
    echo "✅ Archived evolution"
    rm $EVOLUTION_FILES
fi

echo "✅ Archive complete!"
