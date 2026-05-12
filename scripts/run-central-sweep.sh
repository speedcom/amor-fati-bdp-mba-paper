#!/usr/bin/env bash
set -euo pipefail

# Run from a patched amor-fati repository root after `sbt assembly`.
JAR="${JAR:-target/scala-3.8.2/amor-fati.jar}"
SEEDS="${SEEDS:-10}"
MONTHS="${MONTHS:-60}"

if [[ ! -f "$JAR" ]]; then
  echo "JAR not found: $JAR" >&2
  echo "Run sbt assembly first or set JAR=/path/to/amor-fati.jar" >&2
  exit 1
fi

for BDP in 0 500 1000 1500 2000 2500 3000; do
  if [[ "$BDP" == "0" ]]; then
    java -jar "$JAR" "$SEEDS" robust-bdp-0000 \
      --duration "$MONTHS" \
      --run-id "robust-bdp-0000-${MONTHS}m-${SEEDS}s"
  else
    java -jar "$JAR" "$SEEDS" "robust-l050-bdp-${BDP}" \
      --duration "$MONTHS" \
      --run-id "robust-l050-bdp-${BDP}-${MONTHS}m-${SEEDS}s" \
      --bdp "$BDP" \
      --bdp-lambda 0.5
  fi
done
