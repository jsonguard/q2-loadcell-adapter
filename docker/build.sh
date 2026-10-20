#!/bin/sh
set -eu

SRC=/src/q2_loadcell
OUT=/tmp/out
NAME=q2_loadcell
ARCHIVE=q2_loadcell-cp39-aarch64-linux-gnu.tar.gz

[ -d "$SRC" ] || { echo "error: $SRC not mounted" >&2; exit 1; }

cd /tmp
rm -rf "$OUT"
mkdir -p "$OUT" /dist

python3.9 -m nuitka \
    --mode=package \
    --no-pyi-file \
    --assume-yes-for-downloads \
    --deployment \
    --python-flag=no_docstrings,no_asserts \
    --lto=yes \
    --output-dir="$OUT" \
    "$SRC"

BUILT=$(find "$OUT" -maxdepth 1 -name "${NAME}*.so" | head -n1)
[ -n "$BUILT" ] || { echo "error: nuitka produced no .so" >&2; exit 1; }

mv "$BUILT" "$OUT/${NAME}.so"

readelf -d "$OUT/${NAME}.so" | grep NEEDED || true

tar -C "$OUT" -czf "/dist/${ARCHIVE}" "${NAME}.so"
echo "wrote /dist/${ARCHIVE}"
tar -tzf "/dist/${ARCHIVE}"
