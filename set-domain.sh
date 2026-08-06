#!/usr/bin/env bash
# 배포할 도메인으로 한 번에 바꿉니다.
#   ./set-domain.sh https://jeju.mydomain.com
set -euo pipefail
[ $# -eq 1 ] || { echo "사용법: ./set-domain.sh https://your-domain.com"; exit 1; }
NEW="${1%/}"
OLD="https://jeju.example.com"
for f in index.html sitemap.xml robots.txt; do
  if grep -q "$OLD" "$f"; then
    perl -pi -e "s{\Q$OLD\E}{$NEW}g" "$f"
    echo "updated $f"
  fi
done
echo "done -> $NEW"
