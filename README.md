# 半導体顧客向け基本設計書サイト（Zensical版）

[Zensical](https://zensical.org/) で構築した基本設計書サイト。
**設計書の中身は正本（MkDocs版 `C:\DOC\sc-docs-lyr`）と完全に同じ**で、このリポジトリはサイトの見せ方だけを持つ。

- 正本: https://github.com/okakaLDS/sc-docs-lyr （設計書の編集はすべて正本で行う）
- 関連: VitePress版 `C:\DOC\sc-docs-lyr-vitepress`

## このリポジトリで編集してよいもの

| 場所 | 内容 |
| ---- | ---- |
| `zensical.toml` | サイト設定（`nav` は自動生成なので除く） |
| `overrides/` | テーマの上書き（ホームのヒーロー・章カード、メタ情報バー、告知バナー） |
| `docs/assets/zensical/` | Zensical版専用のCSS・JS・アイコン |
| `tools/sync_docs.py` | 正本からの同期スクリプト |

**`docs/` のそれ以外（章フォルダ・`index.md` 等）は直接編集しない**。正本を直して同期する。

## 正本からの同期

```bash
.venv/Scripts/python.exe tools/sync_docs.py
```

- 正本の `docs/` をミラーする（正本で消したファイルはこちらでも消える。`docs/assets/` は対象外）
- 正本の `.pages`（awesome-pages）を読み、`zensical.toml` の `nav` を生成する
  （Zensicalは awesome-pages 未対応のため）。正本と同じ表示順・章タイトルになる
- 正本の場所が違う場合は `--src <正本のdocs>` を付ける

## ローカルプレビュー

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/zensical.exe serve
```

http://127.0.0.1:8001/sc-docs-lyr-zensical/ で確認（MkDocs版の8000番と同時に起動できるよう8001番）。
ビルドは `.venv/Scripts/zensical.exe build --clean`（約2〜5秒）。

## Zensicalの機能の使いどころ

| 機能 | 設定 | 狙い |
| ---- | ---- | ---- |
| llms.txt / llms-full.txt | `[project.plugins.llmstxt]` | 保守工程で生成AIに読ませる前提に合わせ、目次と全文を機械可読で出力。章ごとにセクション分け |
| Markdownコピー | `content.action.copy` | 各ページのMarkdown原文をワンクリックでコピー（AIへの貼り付け用） |
| 編集・原文表示 | `content.action.edit` / `view` | 正本リポジトリの該当ファイルを開く |
| 検索 | 標準 | 日本語の全文検索。タグで絞り込める |
| タグ | `[project.plugins.tags]` | front matter の `tags` を横断一覧（`/tags/`） |
| ページステータス | `[project.extra.status]` | front matter の `status`（作業中／レビュー中／確定）をサイドバーにアイコン表示 |
| Mermaid | superfences | 追加JSなしで描画。配色はテーマに自動で追従 |
| インスタントナビ | `navigation.instant*` | ページ遷移をSPA化、ホバーで先読み |
| 章タブ・パンくず | `navigation.tabs.sticky` / `path` | 章（成果物一覧の項番）を常に上部に表示 |
| テーマ上書き | `overrides/main.html` | ホームのヒーロー・章カード（ナビから自動生成）、各ページ上部に文書番号・担当・状態 |

## デザイン（Zensical版独自）

正本の配色・装飾は引き継がず、半導体の技術資料（データシート）を下敷きにした製図調にしている。
定義は `docs/assets/zensical/site.css`。

- 配色: インク（紺）＋コバルト（リンク・操作）＋銅（アクセント）。ダークモード対応
- 書体: IBM Plex Sans JP ／ IBM Plex Mono（文書番号・ID）
- レイアウト: ブラウザの横幅いっぱいに表示（`.md-grid { max-width: none }`）
- ナビ: `[使い方]`／`[Template]`／`[Sample]` を種別バッジで表示（`site.js`）。表は見出しクリックで並べ替え（tablesort）
- 担当チップの色: KCCS＝コバルト、SC様＝銅、Rikkei＝ティール

## 正本と挙動が違う点・既知の注意

- `attr_list` 拡張は無効。見出し末尾の `{機能ID}` 等のプレースホルダーが属性として消えるため
- 正本の `stylesheets/extra.css`・`javascripts/extra.js` は同期されるが読み込まない。
  表紙の押印枠（`.seal-table`／`.seal-box`）だけ `site.css` に移植している
- ビルド時にアンカー切れの警告が2件出る（正本側の問題。MkDocs版では検出されていない）:
  `04-共通機能設計書/4-1_共通機能一覧/[使い方]4-1_共通機能一覧.md` 220・222行目の
  `#21-共通機能定義一覧`／`#22-使用マトリクス`。見出しは「— サンプル様式」付きのため実際のアンカーと一致しない。
  このため CI では `--strict` を付けていない
- `git-revision-date`（最終更新日）は Zensical 側が未対応（ロードマップ上は予定）

## デプロイ

`.github/workflows/deploy.yml` が main への push で GitHub Pages にデプロイする
（`site_url` は `https://okakalds.github.io/sc-docs-lyr-zensical/` を想定）。
GitHubリポジトリは未作成。作成後、Settings → Pages → Source を「GitHub Actions」にする。
