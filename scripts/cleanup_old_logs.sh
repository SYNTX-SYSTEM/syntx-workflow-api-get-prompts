#!/bin/bash
# Cleanup Old Logs Script
LOGS_DIR="/opt/syntx-config/logs"
DAYS_TO_KEEP=7

echo "=========================================="
echo "Cleanup Old Logs: $(date)"
echo "=========================================="

DELETED=0

for file in "$LOGS_DIR"/field_flow.????????.jsonl; do
    [ -f "$file" ] || continue
    if [ $(find "$file" -mtime +$DAYS_TO_KEEP 2>/dev/null | wc -l) -gt 0 ]; then
        rm "$file"
        echo "🗑️  Deleted: $(basename $file)"
        ((DELETED++))
    fi
done

for file in "$LOGS_DIR"/wrapper_requests.????????.jsonl; do
    [ -f "$file" ] || continue
    if [ $(find "$file" -mtime +$DAYS_TO_KEEP 2>/dev/null | wc -l) -gt 0 ]; then
        rm "$file"
        echo "🗑️  Deleted: $(basename $file)"
        ((DELETED++))
    fi
done

for file in "$LOGS_DIR"/evolution.????????.jsonl; do
    [ -f "$file" ] || continue
    if [ $(find "$file" -mtime +$DAYS_TO_KEEP 2>/dev/null | wc -l) -gt 0 ]; then
        rm "$file"
        echo "🗑️  Deleted: $(basename $file)"
        ((DELETED++))
    fi
done

[ $DELETED -eq 0 ] && echo "✅ No old files" || echo "✅ Deleted $DELETED files"
