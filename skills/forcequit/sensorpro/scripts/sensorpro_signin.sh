#!/usr/bin/env bash
set -euo pipefail

: "${SENSORPRO_API_KEY:?Missing SENSORPRO_API_KEY}"
: "${SENSORPRO_ORG:?Missing SENSORPRO_ORG}"
: "${SENSORPRO_USER:?Missing SENSORPRO_USER}"
: "${SENSORPRO_PASS:?Missing SENSORPRO_PASS}"

curl -sS -X POST "https://apinie.sensorpro.net/auth/sys/signin" \
  -H "Content-Type: application/json" \
  -H "x-apikey: ${SENSORPRO_API_KEY}" \
  -d "{\"Organization\":\"${SENSORPRO_ORG}\",\"User\":\"${SENSORPRO_USER}\",\"Password\":\"${SENSORPRO_PASS}\"}" \
| python3 -c 'import sys,json; j=json.load(sys.stdin); print(j.get("Token",""))'
