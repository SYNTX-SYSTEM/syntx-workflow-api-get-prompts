#!/bin/bash
# Daily Log Rotation Script
LOGS_DIR="/opt/syntx-config/logs"
DATE=$(date +%Y%m%d)

echo "=========================================="
echo "Daily Log Rotation: $(date)"
echo "=========================================="

if [ -f "$LOGS_DIR/field_flow.jsonl" ] && [ -s "$LOGS_DIR/field_flow.jsonl" ]; then
    mv "$LOGS_DIR/field_flow.jsonl" "$LOGS_DIR/field_flow.$DATE.jsonl"
    touch "$LOGS_DIR/field_flow.jsonl"
    echo "✅ Rotated field_flow.jsonl"
fi

if [ -f "$LOGS_DIR/wrapper_requests.jsonl" ] && [ -s "$LOGS_DIR/wrapper_requests.jsonl" ]; then
    mv "$LOGS_DIR/wrapper_requests.jsonl" "$LOGS_DIR/wrapper_requests.$DATE.jsonl"
    touch "$LOGS_DIR/wrapper_requests.jsonl"
    echo "✅ Rotated wrapper_requests.jsonl"
fi

if [ -f "$LOGS_DIR/evolution.jsonl" ] && [ -s "$LOGS_DIR/evolution.jsonl" ]; then
    mv "$LOGS_DIR/evolution.jsonl" "$LOGS_DIR/evolution.$DATE.jsonl"
    touch "$LOGS_DIR/evolution.jsonl"
    echo "✅ Rotated evolution.jsonl"
fi

echo "✅ Daily rotation complete!"
