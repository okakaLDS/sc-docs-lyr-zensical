"""正本（MkDocs版 sc-docs-lyr）の docs/ をこのリポジトリへ同期する。

やること:
  1. 正本の docs/ を ./docs/ へミラーする（正本に無いファイルは削除）。
     ただし ./docs/assets/ はZensical版専用の資産なので触らない。
     awesome-pages 用の .pages はコピーしない（Zensicalは未対応）。
  2. 正本の .pages を読み、zensical.toml のナビゲーション（nav）を生成して
     「# >>> nav (generated)」〜「# <<< nav (generated)」の間を書き換える。

設計書の中身は正本でのみ編集する（このリポジトリの docs/ を直接直さない）。

使い方:
  python tools/sync_docs.py                       # 既定: ../sc-docs-lyr/docs
  python tools/sync_docs.py --src C:/DOC/sc-docs-lyr/docs
  python tools/sync_docs.py --nav-only            # ナビだけ再生成
"""

from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "docs"
CONFIG = ROOT / "zensical.toml"
PROTECTED = {"assets"}  # docs/ 直下でZensical版が所有するフォルダ
SKIP_NAMES = {".pages"}

NAV_BEGIN = "# >>> nav (generated)"
NAV_END = "# <<< nav (generated)"


# ---------------------------------------------------------------------------
# 1. ミラー
# ---------------------------------------------------------------------------
def mirror(src: Path) -> tuple[int, int, int]:
    copied = updated = removed = 0
    src_files = {
        p.relative_to(src)
        for p in src.rglob("*")
        if p.is_file() and p.name not in SKIP_NAMES
    }
    for rel in sorted(src_files):
        if rel.parts[0] in PROTECTED:
            print(f"  ! 正本側の docs/{rel.as_posix()} は保護対象と衝突するためスキップ")
            continue
        s, d = src / rel, DEST / rel
        if d.exists():
            if filecmp.cmp(s, d, shallow=False):
                continue
            updated += 1
        else:
            copied += 1
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)

    for p in sorted(DEST.rglob("*"), reverse=True):
        rel = p.relative_to(DEST)
        if rel.parts[0] in PROTECTED:
            continue
        if p.is_file() and rel not in src_files:
            p.unlink()
            removed += 1
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    return copied, updated, removed


# ---------------------------------------------------------------------------
# 2. .pages → nav
# ---------------------------------------------------------------------------
def read_pages(directory: Path) -> tuple[str | None, list | None]:
    """awesome-pages の .pages から title と nav を読む（このリポジトリで使う書式のみ）。

    対応している書式:
      title: タイトル
      nav:
        - "名前"            # ファイルまたはフォルダ
        - 表示名: パス       # 表示名つき
    """
    f = directory / ".pages"
    if not f.exists():
        return None, None
    title, nav = None, None
    for raw in f.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if m := re.match(r"^title:\s*(.+)$", line):
            title = unquote(m.group(1))
        elif re.match(r"^nav:\s*$", line):
            nav = []
        elif (m := re.match(r"^\s+-\s+(.+)$", line)) and nav is not None:
            item = m.group(1).strip()
            km = re.match(r'^("[^"]+"|[^"]+?):\s+(.+)$', item)
            if re.fullmatch(r'"[^"]*"', item) or not km:
                nav.append(unquote(item))
            else:
                nav.append({unquote(km.group(1)): unquote(km.group(2))})
        else:
            sys.exit(f".pages の未対応の書式: {f}: {raw!r}")
    return title, nav


def unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def natural_key(name: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def build_section(src: Path, directory: Path) -> list:
    """フォルダ1つ分の nav を作る。.pages が無ければ index.md 先頭＋自然順。"""
    _, nav = read_pages(directory)
    if nav is None:
        names = [
            p.name
            for p in directory.iterdir()
            if (p.is_dir() and has_markdown(p)) or p.suffix == ".md"
        ]
        names.sort(key=lambda n: (n != "index.md", natural_key(n)))
        nav = names
    items = []
    for entry in nav:
        if isinstance(entry, dict):
            (label, target), = entry.items()
            items.append({label: rel_path(src, directory / target)})
            continue
        target = directory / entry
        if target.is_dir():
            title, _ = read_pages(target)
            items.append({title or entry: build_section(src, target)})
        elif target.is_file():
            items.append(rel_path(src, target))
        else:
            sys.exit(f".pages が存在しない項目を指している: {directory / '.pages'}: {entry}")
    return items


def has_markdown(directory: Path) -> bool:
    return any(directory.rglob("*.md"))


def rel_path(src: Path, p: Path) -> str:
    return p.relative_to(src).as_posix()


def to_toml(items: list, indent: int = 1) -> str:
    pad = "  " * indent
    lines = []
    for item in items:
        if isinstance(item, str):
            lines.append(f"{pad}{q(item)},")
        else:
            (label, value), = item.items()
            if isinstance(value, str):
                lines.append(f"{pad}{{ {q(label)} = {q(value)} }},")
            else:
                lines.append(f"{pad}{{ {q(label)} = [")
                lines.append(to_toml(value, indent + 1))
                lines.append(f"{pad}] }},")
    return "\n".join(lines)


def q(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def write_nav(src: Path) -> int:
    nav = build_section(src, src)
    block = f"{NAV_BEGIN}\n# tools/sync_docs.py が正本の .pages から生成。手で編集しない。\nnav = [\n{to_toml(nav)}\n]\n{NAV_END}"
    text = CONFIG.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END), re.S)
    if not pattern.search(text):
        sys.exit(f"zensical.toml に {NAV_BEGIN} 〜 {NAV_END} のマーカーが無い")
    CONFIG.write_text(pattern.sub(lambda _: block, text), encoding="utf-8", newline="\n")
    return block.count(".md")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", type=Path, default=ROOT.parent / "sc-docs-lyr" / "docs")
    ap.add_argument("--nav-only", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    src = args.src.resolve()
    if not (src / ".pages").exists():
        sys.exit(f"正本の docs/ が見つからない（.pages が無い）: {src}")

    print(f"正本: {src}")
    if not args.nav_only:
        c, u, r = mirror(src)
        print(f"  docs/ 同期: 追加 {c} / 更新 {u} / 削除 {r}")
    n = write_nav(src)
    print(f"  nav 生成: {n} ページ")


if __name__ == "__main__":
    main()
