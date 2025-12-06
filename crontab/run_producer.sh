#!/bin/bash
# Producer Wrapper - Loads .env and runs producer

cd /opt/syntx-workflow-api-get-prompts

# Load .env if exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run producer
/usr/bin/python3 evolution/evolutionary_producer.py
