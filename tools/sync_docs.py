"""正本（MkDocs版 sc-docs-lyr）の docs/ をこのリポジトリへ同期する。

やること:
  1. 正本の docs/ を ./docs/ へ反映する（正本に無いファイルは削除）。
     ./docs/assets/ はZensical版専用の資産なので触らない。
     awesome-pages 用の .pages はコピーしない（Zensicalは未対応）。
  2. 正本の .pages を読み、zensical.toml のナビゲーション（nav）を生成して
     「# >>> nav (generated)」〜「# <<< nav (generated)」の間を書き換える。

構成（--layout）:
  sample-flat（既定）… 各ドキュメントの [Sample] だけを載せ、階層を浅くする。
      - [使い方]／[Template] のページは載せない
      - 章フォルダ以外で、中身が1ファイルだけになるフォルダはそのファイルを1階層上へ移す
        （index.md だけが残る場合は「フォルダ名.md」にする）
      - 移動したページへのリンクは張り替える。載せないページへのリンクは
        同じドキュメントの [Sample] へ向け、向け先が無い（自分自身など）場合は地の文にする
      - コードスパン・コードブロック内のリンク（記述例）は書き換えない
  full … 正本のまま（全ページ・同じ階層）

タブ分け（既定で有効、--no-tabs で無効）:
  末尾の「## 文書情報」「## 改定履歴」を本文と別タブにする（pymdownx.blocks.tab）。
  正本はVSCodeで崩れないようタブ記法を使わないので、変換はこの同期時に行う。

設計書の中身は正本でのみ編集する（このリポジトリの docs/ を直接直さない）。

使い方:
  python tools/sync_docs.py                       # 既定: ../sc-docs-lyr/docs, sample-flat
  python tools/sync_docs.py --src C:/DOC/sc-docs-lyr/docs
  python tools/sync_docs.py --layout full
  python tools/sync_docs.py --no-tabs
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote as url_unquote

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "docs"
CONFIG = ROOT / "zensical.toml"
PROTECTED = {"assets"}  # docs/ 直下でZensical版が所有するフォルダ
SKIP_NAMES = {".pages"}
SAMPLE = "[Sample]"

NAV_BEGIN = "# >>> nav (generated)"
NAV_END = "# <<< nav (generated)"


# ---------------------------------------------------------------------------
# .pages → nav（正本の構成）
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
            if (p.is_dir() and any(p.rglob("*.md"))) or p.suffix == ".md"
        ]
        names.sort(key=lambda n: (n != "index.md", natural_key(n)))
        nav = names
    items = []
    for entry in nav:
        if isinstance(entry, dict):
            (label, target), = entry.items()
            items.append({label: rel(src, directory / target)})
            continue
        target = directory / entry
        if target.is_dir():
            title, _ = read_pages(target)
            items.append({title or entry: build_section(src, target)})
        elif target.is_file():
            items.append(rel(src, target))
        else:
            sys.exit(f".pages が存在しない項目を指している: {directory / '.pages'}: {entry}")
    return items


def rel(src: Path, p: Path) -> str:
    return p.relative_to(src).as_posix()


# ---------------------------------------------------------------------------
# sample-flat: どのファイルを載せ、どこへ置くか
# ---------------------------------------------------------------------------
def is_chapter_file(path: str) -> bool:
    """章フォルダ（docs直下の 01-表紙 等）の配下か。docs直下のファイルと images 等は対象外。"""
    parts = PurePosixPath(path).parts
    return len(parts) >= 2 and re.match(r"^\d{2}-", parts[0]) is not None


def plan_sample_flat(files: list[str]) -> dict[str, str]:
    """正本の相対パス → 出力先の相対パス（載せないファイルは含めない）。"""
    kept = []
    for f in files:
        if not is_chapter_file(f):
            kept.append(f)
        elif f.endswith(".md"):
            if any(part.startswith(SAMPLE) for part in PurePosixPath(f).parts):
                kept.append(f)
        else:
            kept.append(f)  # 図などのmd以外はそのまま（参照先として残す）

    mapping = {f: f for f in kept}
    md = [f for f in kept if f.endswith(".md") and is_chapter_file(f)]

    # 深いフォルダから順に、mdが1つだけのフォルダを畳む（章フォルダは畳まない）
    changed = True
    while changed:
        changed = False
        current = {}
        for f in md:
            current.setdefault(str(PurePosixPath(mapping[f]).parent), []).append(f)
        subdirs = {}
        for d in current:
            p = PurePosixPath(d)
            for i in range(1, len(p.parts)):
                subdirs.setdefault(str(PurePosixPath(*p.parts[:i])), set()).add(d)
        for d in sorted(current, key=lambda d: -len(PurePosixPath(d).parts)):
            p = PurePosixPath(d)
            if len(p.parts) < 2:  # 章フォルダ
                continue
            has_child_dirs = any(x != d for x in subdirs.get(d, ()))
            if len(current[d]) == 1 and not has_child_dirs:
                f = current[d][0]
                name = PurePosixPath(mapping[f]).name
                if name == "index.md":
                    name = p.name + ".md"
                mapping[f] = str(p.parent / name)
                changed = True
                break
    return mapping


def sample_fallback(files_kept: list[str]) -> dict[str, str]:
    """正本のフォルダ → そのフォルダの最初の [Sample] ページ（載せないページへのリンクの向け先）。"""
    by_dir: dict[str, list[str]] = {}
    for f in files_kept:
        if not f.endswith(".md"):
            continue
        p = PurePosixPath(f)
        # [Sample]フォルダ配下なら、そのフォルダ自体を元フォルダの代表にする
        for i, part in enumerate(p.parts):
            if part.startswith(SAMPLE):
                by_dir.setdefault(str(PurePosixPath(*p.parts[:i])), []).append(f)
                break
    result = {}
    for d, fs in by_dir.items():
        # 浅いもの → index.md → 自然順
        fs.sort(key=lambda f: (f.count("/"), PurePosixPath(f).name != "index.md", natural_key(f)))
        result[d] = fs[0]
    return result


# ---------------------------------------------------------------------------
# リンクの張り替え
# ---------------------------------------------------------------------------
# リンク文字列中の \[ \] （エスケープした角括弧）も1文字として扱う
LINK = re.compile(r"(?<!!)\[(?P<text>(?:\\.|[^\]\n])*)\]\((?P<target><[^>\n]+>|[^)\s]+)\)")
IMAGE = re.compile(r"!\[(?P<text>(?:\\.|[^\]\n])*)\]\((?P<target><[^>\n]+>|[^)\s]+)\)")


def rewrite_links(text: str, old: str, new: str, mapping: dict[str, str],
                  fallback: dict[str, str], removed_dirs: dict[str, str]) -> str:
    old_dir = posixpath.dirname(old)
    new_dir = posixpath.dirname(new)

    def resolve(target: str) -> tuple[str, str] | None:
        if re.match(r"^[a-z]+:|^#|^/", target):
            return None
        path, _, anchor = target.partition("#")
        if not path:
            return None
        return posixpath.normpath(posixpath.join(old_dir, url_unquote(path))), anchor

    def relto(dest: str, anchor: str) -> str:
        r = posixpath.relpath(dest, new_dir or ".")
        return r + (f"#{anchor}" if anchor else "")

    def fmt(target: str, angle: bool) -> str:
        return f"<{target}>" if angle or re.search(r"[\s()<>]", target) else target

    def on_link(m: re.Match, image: bool) -> str:
        raw = m.group("target")
        angle = raw.startswith("<")
        target = raw[1:-1] if angle else raw
        r = resolve(target)
        if r is None:
            return m.group(0)
        dest, anchor = r
        prefix = "!" if image else ""
        if dest in mapping:
            new_target = relto(mapping[dest], anchor)
            if new_target == target:
                return m.group(0)
            return f"{prefix}[{m.group('text')}]({fmt(new_target, angle)})"
        if image or not dest.endswith(".md"):
            return m.group(0)
        # 載せないページ → 同じドキュメントの Sample へ。自分自身なら地の文
        sample = fallback.get(removed_dirs.get(dest, posixpath.dirname(dest)))
        if sample and mapping[sample] != new:
            return f"[{m.group('text')}]({fmt(relto(mapping[sample], ''), angle)})"
        return m.group("text")

    out, fence = [], None
    for line in text.split("\n"):
        stripped = line.lstrip()
        if fence:
            out.append(line)
            if stripped.startswith(fence):
                fence = None
            continue
        if fm := re.match(r"^(`{3,}|~{3,})", stripped):
            fence = fm.group(1)
            out.append(line)
            continue
        # インラインコードの中は書き換えない
        parts = re.split(r"(`+[^`]*`+)", line)
        for i in range(0, len(parts), 2):
            parts[i] = IMAGE.sub(lambda m: on_link(m, True), parts[i])
            parts[i] = LINK.sub(lambda m: on_link(m, False), parts[i])
        out.append("".join(parts))
    return "\n".join(out)


# ---------------------------------------------------------------------------
# nav の変換（sample-flat）
# ---------------------------------------------------------------------------
def transform_nav(items: list, mapping: dict[str, str], depth: int = 0) -> list:
    result = []
    for item in items:
        if isinstance(item, str):
            if item in mapping:
                result.append(mapping[item])
            continue
        (label, value), = item.items()
        if isinstance(value, str):
            if value in mapping:
                result.append({label: mapping[value]})
            continue
        children = transform_nav(value, mapping, depth + 1)
        if not children:
            continue
        label = label.replace(SAMPLE, "")
        # 章（depth 0）以外で1ページだけになったセクションは、そのページに置き換える
        if depth >= 1 and len(children) == 1 and isinstance(children[0], str):
            result.append(children[0])
        else:
            result.append({label: children})
    return result


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


def write_nav(nav: list, layout: str) -> int:
    block = (f"{NAV_BEGIN}\n# tools/sync_docs.py（--layout {layout}）が正本の .pages から生成。手で編集しない。\n"
             f"nav = [\n{to_toml(nav)}\n]\n{NAV_END}")
    text = CONFIG.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END), re.S)
    if not pattern.search(text):
        sys.exit(f"zensical.toml に {NAV_BEGIN} 〜 {NAV_END} のマーカーが無い")
    CONFIG.write_text(pattern.sub(lambda _: block, text), encoding="utf-8", newline="\n")
    return block.count(".md")


# ---------------------------------------------------------------------------
# 反映
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 文書情報・改定履歴のタブ分け
# ---------------------------------------------------------------------------
TAIL_SECTIONS = ("文書情報", "改定履歴", "改訂履歴")


def split_tabs(text: str) -> str:
    """末尾の「## 文書情報」「## 改定履歴」を本文と別タブにする（pymdownx.blocks.tab）。

    対象は、ファイル末尾に連続して並ぶこれらの見出しの節だけ。
    「5. 改訂履歴（設計内容）」のような番号付きの本文節は対象外（設計内容の一部）。
    h1（ページタイトル）はタブの外に残す。直前の区切り線 --- は取り除く。
    """
    lines = text.split("\n")
    h1 = None
    h2: list[tuple[int, str]] = []
    fence = None
    start = 0
    if lines and lines[0] == "---":  # front matter
        start = lines.index("---", 1) + 1
    for i in range(start, len(lines)):
        stripped = lines[i].lstrip()
        if fence:
            if stripped.startswith(fence):
                fence = None
            continue
        if fm := re.match(r"^(`{3,}|~{3,})", stripped):
            fence = fm.group(1)
            continue
        if lines[i].startswith("# ") and h1 is None:
            h1 = i
        elif lines[i].startswith("## "):
            h2.append((i, lines[i][3:].strip()))

    k = len(h2)
    while k > 0 and h2[k - 1][1] in TAIL_SECTIONS:
        k -= 1
    if k == len(h2):
        return text
    cut = h2[k][0]
    label = "・".join(name for _, name in h2[k:])

    body_start = h1 + 1 if h1 is not None and h1 < cut else start
    body = lines[body_start:cut]
    while body and body[-1].strip() in ("", "---"):
        body.pop()
    meta = lines[cut:]
    while meta and not meta[-1].strip():
        meta.pop()
    return "\n".join(
        lines[:body_start]
        + ["", "/// tab | 本文", ""] + body + ["", "///", ""]
        + [f"/// tab | {label}", ""] + meta + ["", "///", ""]
    )


def sync(src: Path, layout: str, tabs: bool) -> list:
    files = sorted(
        rel(src, p) for p in src.rglob("*")
        if p.is_file() and p.name not in SKIP_NAMES and p.relative_to(src).parts[0] not in PROTECTED
    )
    if layout == "full":
        mapping = {f: f for f in files}
        fallback, removed_dirs = {}, {}
    else:
        mapping = plan_sample_flat(files)
        fallback = sample_fallback(list(mapping))
        # 載せないページの「ドキュメント」＝ [使い方]/[Template] が属するフォルダ。
        # [Template]xxx/ フォルダ配下ならそのフォルダの親
        removed_dirs = {}
        for f in files:
            if f in mapping or not f.endswith(".md"):
                continue
            p = PurePosixPath(f)
            for i, part in enumerate(p.parts):
                if part.startswith(("[使い方]", "[Template]")):
                    removed_dirs[f] = str(PurePosixPath(*p.parts[:i]))
                    break

    outputs: dict[str, bytes] = {}
    for old, new in mapping.items():
        data = (src / old).read_bytes()
        if old.endswith(".md") and (layout != "full" or tabs):
            text = data.decode("utf-8")
            if layout != "full":
                text = rewrite_links(text, old, new, mapping, fallback, removed_dirs)
            if tabs:
                text = split_tabs(text)
            data = text.encode("utf-8")
        if new in outputs:
            sys.exit(f"出力先が衝突: {new}")
        outputs[new] = data

    added = updated = removed = 0
    for new, data in outputs.items():
        d = DEST / new
        if d.exists():
            if d.read_bytes() == data:
                continue
            updated += 1
        else:
            added += 1
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(data)
    for p in sorted(DEST.rglob("*"), reverse=True):
        r = p.relative_to(DEST)
        if r.parts[0] in PROTECTED:
            continue
        if p.is_file() and r.as_posix() not in outputs:
            p.unlink()
            removed += 1
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    print(f"  docs/ 反映: 追加 {added} / 更新 {updated} / 削除 {removed}（{len(outputs)} ファイル）")

    nav = build_section(src, src)
    return nav if layout == "full" else transform_nav(nav, mapping)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", type=Path, default=ROOT.parent / "sc-docs-lyr" / "docs")
    ap.add_argument("--layout", choices=["sample-flat", "full"], default="sample-flat")
    ap.add_argument("--no-tabs", action="store_true", help="文書情報・改定履歴のタブ分けをしない")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    src = args.src.resolve()
    if not (src / ".pages").exists():
        sys.exit(f"正本の docs/ が見つからない（.pages が無い）: {src}")

    print(f"正本: {src}（--layout {args.layout}）")
    nav = sync(src, args.layout, tabs=not args.no_tabs)
    n = write_nav(nav, args.layout)
    print(f"  nav 生成: {n} ページ")


if __name__ == "__main__":
    main()
