#!/usr/bin/env bash
# Call a Sensorpro endpoint with a JSON body, automatically handling signin+logoff.
#
# Usage:
#   sensorpro_call.sh <url-with-[Token]-slot> <json-body>
# Example:
#   sensorpro_call.sh "https://apinie.sensorpro.net/api/Contact/UpdateAdd/[Token]" '{"AddToList":[],...}'
set -euo pipefail

URL_TEMPLATE="${1:-}"
BODY="${2:-}"

if [[ -z "$URL_TEMPLATE" || -z "$BODY" ]]; then
  echo "Usage: $0 <url-with-[Token]> <json-body>" >&2
  exit 2
fi

TOKEN="$("$(dirname "$0")/sensorpro_signin.sh")"
if [[ -z "$TOKEN" ]]; then
  echo "Signin failed: empty token" >&2
  exit 1
fi

URL="${URL_TEMPLATE//\[Token\]/$TOKEN}"

# Call
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  --data-binary "$BODY"

# Best-effort logoff (requires body on some servers)
curl -sS -X POST "https://apinie.sensorpro.net/auth/sys/logoff/${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}' >/dev/null 2>&1 || true
