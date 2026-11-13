#!/usr/bin/env bash
# install.sh — cài (boot) toàn bộ skill trong Mark85skill vào Claude Code và dsh.
# Chạy lại bao nhiêu lần cũng được: symlink được làm mới, bản cũ không phải symlink thì backup trước khi thay.
#
#   ./install.sh            # cài cả hai
#   ./install.sh --dry-run  # chỉ in ra sẽ làm gì
#
# Đích:
#   Claude Code : ${CLAUDE_SKILLS_DIR:-~/.claude/skills}/<name>        (thư mục chứa SKILL.md)
#   dsh         : ${DSH_HOME:-~/.dsh}/skills/<name>                    (thư mục chứa SKILL.md hoặc file <name>.md)
# Skill thường  -> symlink tới Mark85skill/<name> (sửa một chỗ, cả hai harness thấy ngay).
# AI-Factory    -> sinh bản cài "factory" từ AI-Factory/skills/factory.md, thay <bundle> bằng đường dẫn tuyệt đối.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CC_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DSH_DIR="${DSH_HOME:-$HOME/.dsh}/skills"
BACKUP="$SRC/.backup/$(date +%Y%m%d-%H%M%S)"
DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1

run() { if ((DRY)); then echo "  [dry] $*"; else "$@"; fi; }

backup_if_real() {   # $1 = đường dẫn đích; backup nếu tồn tại và không phải symlink
  local t="$1"
  if [[ -e "$t" && ! -L "$t" ]]; then
    local rel="${t#/}"; run mkdir -p "$BACKUP/$(dirname "$rel")"
    echo "  backup $t -> $BACKUP/$rel"; run mv "$t" "$BACKUP/$rel"
  fi
}

link() {   # $1 = nguồn, $2 = đích
  backup_if_real "$2"
  run ln -sfn "$1" "$2"
  echo "  link $2 -> $1"
}

gen_factory() {   # $1 = file đích
  local out="$1" bundle="$SRC/AI-Factory"
  # bản do chính script này sinh (đã chứa đường dẫn bundle hiện tại) thì ghi đè luôn, không backup
  grep -qF "$bundle" "$out" 2>/dev/null || backup_if_real "$out"
  [[ -L "$out" ]] && run rm "$out"
  if ((DRY)); then echo "  [dry] gen $out"; return; fi
  sed "s#<bundle>#${bundle}#g" "$bundle/skills/factory.md" > "$out"
  echo "  gen  $out (bundle=$bundle)"
}

SKILLS=()
for d in "$SRC"/*/; do
  n="$(basename "$d")"
  [[ "$n" == "AI-Factory" || "$n" == .* ]] && continue
  [[ -f "$d/SKILL.md" ]] && SKILLS+=("$n")
done

for target in "$CC_DIR" "$DSH_DIR"; do
  echo "== $target"
  run mkdir -p "$target"
  for n in "${SKILLS[@]}"; do link "$SRC/$n" "$target/$n"; done
done

echo "== AI-Factory (/factory)"
run mkdir -p "$CC_DIR/factory"
gen_factory "$CC_DIR/factory/SKILL.md"
gen_factory "$DSH_DIR/factory.md"

echo "Xong. Claude Code: mở phiên mới (hoặc /skills) để thấy skill. dsh: /skills trong dsh-tui."
