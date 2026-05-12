#!/usr/bin/env bash
set -euo pipefail

# Run from a patched amor-fati repository root after `sbt assembly`.
# The BDP=0 baseline is common; generate it with run-central-sweep.sh.
JAR="${JAR:-target/scala-3.8.2/amor-fati.jar}"
SEEDS="${SEEDS:-10}"
MONTHS="${MONTHS:-60}"

if [[ ! -f "$JAR" ]]; then
  echo "JAR not found: $JAR" >&2
  echo "Run sbt assembly first or set JAR=/path/to/amor-fati.jar" >&2
  exit 1
fi

for SPEC in "000 0.0" "025 0.25" "050 0.5" "075 0.75" "100 1.0"; do
  read -r TAG LAMBDA <<< "$SPEC"

  for BDP in 500 1000 1500 2000 2500 3000; do
    java -jar "$JAR" "$SEEDS" "robust-l${TAG}-bdp-${BDP}" \
      --duration "$MONTHS" \
      --run-id "robust-l${TAG}-bdp-${BDP}-${MONTHS}m-${SEEDS}s" \
      --bdp "$BDP" \
      --bdp-lambda "$LAMBDA"
  done
done
