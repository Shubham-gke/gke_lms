#!/usr/bin/env bash
set -euo pipefail

BENCH="/home/frappe/frappe-bench-lms"
FRONTEND="$BENCH/apps/lms/frontend"
CUSTOM="$BENCH/apps/lms_custom/lms_custom/frontend"
SRC="$FRONTEND/src"
BACKUP="$(mktemp -d)"

FILES=(
  "routes.js"
  "pages/Courses/Courses.vue"
  "pages/SuggestedCourses.vue"
  "pages/ScoreCard.vue"
)

mkdir -p "$BACKUP/original"
touch "$BACKUP/existing.txt"

restore() {
  echo "Restoring original LMS source files..."

  for file in "${FILES[@]}"; do
    if grep -Fxq "$file" "$BACKUP/existing.txt"; then
      mkdir -p "$SRC/$(dirname "$file")"
      cp -p "$BACKUP/original/$file" "$SRC/$file"
    else
      rm -f "$SRC/$file"
    fi
  done

  rm -rf "$BACKUP"
  echo "Original LMS source files restored."
}

for file in "${FILES[@]}"; do
  if [ -f "$SRC/$file" ]; then
    mkdir -p "$BACKUP/original/$(dirname "$file")"
    cp -p "$SRC/$file" "$BACKUP/original/$file"
    echo "$file" >> "$BACKUP/existing.txt"
  fi
done

trap restore EXIT

echo "Applying custom LMS frontend files..."

cp "$CUSTOM/src_override/routes.js" "$SRC/routes.js"
cp "$CUSTOM/src_override/pages/Courses/Courses.vue" \
   "$SRC/pages/Courses/Courses.vue"

cp "$CUSTOM/src/pages/SuggestedCourses.vue" \
   "$SRC/pages/SuggestedCourses.vue"

cp "$CUSTOM/src/pages/ScoreCard.vue" \
   "$SRC/pages/ScoreCard.vue"

echo "Building LMS frontend..."
cd "$FRONTEND"
yarn build

echo "Build command completed."
