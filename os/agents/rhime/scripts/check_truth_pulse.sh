#!/bin/bash
# Rhime Agent - Truth Pulse Check
# Culture Key Diagnostics (v1.0)

echo "🪶 Initiating Rhime Truth Pulse check..."
if grep -q "truth_scan" os/agents/rhime/text_flow.md; then
  echo "✅ Truth scan directive found in text_flow.md"
  echo "Rhime integrity pulse verified."
  exit 0
else
  echo "⚠️ No truth_scan directive found. Integrity uncertain."
  exit 1
fi
