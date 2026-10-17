---
title: "更新条件表"
tags:
  - 機能定義書
owner: "KCCS"
doc_no: "8.1.6"
---

# 更新条件表

## 1. 概要

本機能が更新するテーブルは4つ。削除処理（DELETE）は存在しない。

| 項目               | 内容                       |
| ------------------ | -------------------------- |
| システムID／機能ID | S021G                      |
| 画面ID             | U31                        |
| 作成日／作成者     | 不明（原設計書未受領のため未特定） |

## 2. 更新テーブル一覧

| No. | テーブルID | テーブル名 | 操作 | 契機 | 詳細 |
| --- | ---------- | ---------- | ---- | ---- | ---- |
| 1 | `LYR03_DEF_TBL` | 検索条件保存 | UPDATE / INSERT | 「検索条件保存」ボタン押下 | [02_LYR03_DEF_TBL_検索条件保存.md](LYR03_DEF_TBL_検索条件保存_02.md) |
| 2 | `ISD_HASSOU_TBL` | 海外（ISD）発送予定 | UPDATE | 「更新」ボタン押下（海外行） | [03_ISD_HASSOU_TBL_海外ISD発送予定.md](ISD_HASSOU_TBL_海外ISD発送予定_03.md) |
| 3 | `DSD_HASSOU_TBL` | 国内（DSD）発送予定 | UPDATE | 「更新」ボタン押下（国内行） | [04_DSD_HASSOU_TBL_国内DSD発送予定.md](DSD_HASSOU_TBL_国内DSD発送予定_04.md) |
| 4 | `MEMO_TBL` | 型代（TC）案件メモ管理 | UPDATE | 「更新」ボタン押下（型代行） | [05_MEMO_TBL_型代TC案件メモ管理.md](MEMO_TBL_型代TC案件メモ管理_05.md) |

## 3. 行単位の振り分けロジック

| 優先 | 条件 | 更新先テーブル |
| ---- | ---- | -------------- |
| ① | `TC_CHK == "TC"` | `MEMO_TBL` |
| ② | `KOKUNAI_KAIGAI_KBN == "2"`（海外） | `ISD_HASSOU_TBL` |
| ③ | `KOKUNAI_KAIGAI_KBN == "1"`（国内） | `DSD_HASSOU_TBL` |
| ④ | いずれにも該当しない | 更新なし |

なお、グリッド表示値がDBロード時点の値と同一の行は更新対象外とする。
