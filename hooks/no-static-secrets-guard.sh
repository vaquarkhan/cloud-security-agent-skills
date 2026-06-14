#!/usr/bin/env bash
# Quick scan for static secret patterns in staged files
set -euo pipefail
PATTERNS='AKIA[0-9A-Z]{16}|aws_secret_access_key|client_secret=|AccessKeySecret'
if git diff --cached 2>/dev/null | grep -iE "$PATTERNS"; then
  echo "ERROR: Possible static secret in staged diff. Use IdentityManager / vault." >&2
  exit 1
fi
echo "OK: no obvious static secret patterns in staged diff"
