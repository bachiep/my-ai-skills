#!/usr/bin/env bash
# Cài skill tao_phim_tat_iphone cho agent.
#
# Mỗi agent để skill một chỗ khác nhau, nên script này TỰ PHÁT HIỆN thư mục
# skill của các agent phổ biến trên máy rồi cài vào đó. Muốn chỉ định tay:
#   ./install.sh --target /đường/dẫn/tới/thư-mục-skill
#
# Bản chất skill không phụ thuộc vị trí: chỉ cần copy NGUYÊN thư mục này
# (SKILL.md + bin/ + references/) vào nơi agent đọc skill, rồi cho agent đọc SKILL.md.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
NAME="tao-phim-tat-iphone"

# Các vị trí skill phổ biến (thêm dòng mới khi có agent mới)
CANDIDATES=(
  "$HOME/.claude/skills/$NAME"     # Claude Code
  "$HOME/workspace/skills/$NAME"   # Muse
)

TARGETS=()
if [ "${1:-}" = "--target" ] && [ -n "${2:-}" ]; then
  TARGETS=("$2")
else
  for c in "${CANDIDATES[@]}"; do
    parent="$(dirname "$c")"
    if [ -d "$parent" ]; then
      TARGETS+=("$c")
    fi
  done
  if [ "${#TARGETS[@]}" -eq 0 ]; then
    echo "Không phát hiện thư mục skill của agent nào."
    echo "Dùng: ./install.sh --target /đường/dẫn/tới/thư-mục-skill"
    exit 1
  fi
fi

for t in "${TARGETS[@]}"; do
  mkdir -p "$t"
  cp -r "$SRC/SKILL.md" "$SRC/bin" "$SRC/references" "$t/"
  echo "Đã cài vào: $t"
done
echo "Xong. Cho agent đọc SKILL.md trong thư mục skill rồi làm theo quy trình."
