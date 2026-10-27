# #!/usr/bin/env bash
# set -euo pipefail

# BENCH="$HOME/frappe/frappe-bench"
# FRONTEND="$BENCH/apps/lms/frontend"
# CUSTOM="$BENCH/apps/lms_custom/lms_custom/frontend"
# SRC="$FRONTEND/src"
# BACKUP="$(mktemp -d)"

# FILES=(
#   "routes.js"
#   "pages/Courses/Courses.vue"
#   "pages/SuggestedCourses.vue"
#   "pages/ScoreCard.vue"
# )

# mkdir -p "$BACKUP/original"
# touch "$BACKUP/existing.txt"

# restore() {
#   echo "Restoring original LMS source files..."

#   for file in "${FILES[@]}"; do
#     if grep -Fxq "$file" "$BACKUP/existing.txt"; then
#       mkdir -p "$SRC/$(dirname "$file")"
#       cp -p "$BACKUP/original/$file" "$SRC/$file"
#     else
#       rm -f "$SRC/$file"
#     fi
#   done

#   rm -rf "$BACKUP"
#   echo "Original LMS source files restored."
# }

# for file in "${FILES[@]}"; do
#   if [ -f "$SRC/$file" ]; then
#     mkdir -p "$BACKUP/original/$(dirname "$file")"
#     cp -p "$SRC/$file" "$BACKUP/original/$file"
#     echo "$file" >> "$BACKUP/existing.txt"
#   fi
# done

# trap restore EXIT

# echo "Applying custom LMS frontend files..."

# cp "$CUSTOM/src_override/routes.js" "$SRC/routes.js"
# cp "$CUSTOM/src_override/pages/Courses/Courses.vue" \
#    "$SRC/pages/Courses/Courses.vue"

# cp "$CUSTOM/src/pages/SuggestedCourses.vue" \
#    "$SRC/pages/SuggestedCourses.vue"

# cp "$CUSTOM/src/pages/ScoreCard.vue" \
#    "$SRC/pages/ScoreCard.vue"

# echo "Building LMS frontend..."
# cd "$FRONTEND"
# yarn build

# echo "Build command completed."















#!/usr/bin/env bash
set -Eeuo pipefail

BENCH="$HOME/frappe/frappe-bench/frappe-bench-v16"
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

restore() {
  echo "Restoring original LMS source files..."

  for file in "${FILES[@]}"; do
    if [ -f "$BACKUP/original/$file" ]; then
      mkdir -p "$SRC/$(dirname "$file")"
      cp -p "$BACKUP/original/$file" "$SRC/$file"
    elif [ -f "$BACKUP/missing/$file" ]; then
      rm -f "$SRC/$file"
    fi
  done

  rm -rf "$BACKUP"
}

trap restore EXIT

# Validate paths
if [ ! -d "$FRONTEND" ] || [ ! -d "$CUSTOM" ]; then
  echo "ERROR: LMS ya lms_custom frontend path nahi mila."
  exit 1
fi

# Backup existing files, including files that do not exist
for file in "${FILES[@]}"; do
  if [ -f "$SRC/$file" ]; then
    mkdir -p "$BACKUP/original/$(dirname "$file")"
    cp -p "$SRC/$file" "$BACKUP/original/$file"
  else
    mkdir -p "$BACKUP/missing/$(dirname "$file")"
    touch "$BACKUP/missing/$file"
  fi
done

# Validate custom files
for file in "${FILES[@]}"; do
  if [ ! -f "$CUSTOM/src_override/$file" ] && \
     [ ! -f "$CUSTOM/src/$file" ]; then
    echo "ERROR: Custom file missing: $file"
    exit 1
  fi
done

# Copy custom routes and pages temporarily into LMS source
cp "$CUSTOM/src_override/routes.js" "$SRC/routes.js"
cp "$CUSTOM/src_override/pages/Courses/Courses.vue" \
   "$SRC/pages/Courses/Courses.vue"
cp "$CUSTOM/src/pages/SuggestedCourses.vue" \
   "$SRC/pages/SuggestedCourses.vue"
cp "$CUSTOM/src/pages/ScoreCard.vue" \
   "$SRC/pages/ScoreCard.vue"

echo "Building LMS frontend with lms_custom changes..."
cd "$FRONTEND"
yarn build

echo "Build completed successfully."

