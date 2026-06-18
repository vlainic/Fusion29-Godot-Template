#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="${1:-steam-content}"
WINDOWS_ZIP="${2:-Windows.zip}"
LINUX_ZIP="${3:-LinuxX11.zip}"

mkdir -p "${OUTPUT_DIR}/windows" "${OUTPUT_DIR}/linux"

unzip -o -q "${WINDOWS_ZIP}" -d "${OUTPUT_DIR}/windows"
unzip -o -q "${LINUX_ZIP}" -d "${OUTPUT_DIR}/linux"

if [ ! -f "${OUTPUT_DIR}/windows/game.exe" ]; then
  echo "Missing ${OUTPUT_DIR}/windows/game.exe after extracting ${WINDOWS_ZIP}" >&2
  exit 1
fi

if [ ! -f "${OUTPUT_DIR}/linux/game.x86_64" ]; then
  echo "Missing ${OUTPUT_DIR}/linux/game.x86_64 after extracting ${LINUX_ZIP}" >&2
  exit 1
fi

echo "Steam content ready under ${OUTPUT_DIR}/"
