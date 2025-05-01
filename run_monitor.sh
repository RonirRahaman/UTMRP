#!/bin/bash

echo "🛡️ Running UTMRP - Linux Threat Monitor"

# Run log parser
echo "🔍 Parsing logs..."
./scripts/parse_logs.py

# Generate full report
echo "📝 Generating full report..."
./scripts/generate_report.py

echo "✅ All done. Check the logs/ directory for the latest report."
