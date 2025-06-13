#!/bin/bash
set -e

REPO_URL="https://github.com/philippxmeyer/RaspiZeroCam.git"
TARGET_DIR="$HOME/RaspiZeroCam"

if [ ! -d "$TARGET_DIR" ]; then
    git clone "$REPO_URL" "$TARGET_DIR"
else
    echo "$TARGET_DIR exists, pulling latest changes"
    git -C "$TARGET_DIR" pull
fi

cd "$TARGET_DIR"
./install.sh
