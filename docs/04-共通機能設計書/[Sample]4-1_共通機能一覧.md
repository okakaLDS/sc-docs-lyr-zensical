---
title: "共通機能一覧（サンプル）"
tags:
  - 共通機能
status: "作業中"
owner: "KCCS"
doc_no: "4.1"
---
# 共通機能一覧 — サンプル

/// tab | 本文


## 1. 凡例（使用マトリクス記号）

| 記号     | 意味   |
| -------- | ------ |
| ●       | 使用   |
| （空欄） | 未使用 |

## 2. 共通機能一覧（ロジック共通化）

ソースコードの`com/`フォルダー配下にあり、2つ以上の機能（OPFパッケージ）から呼び出されるクラス・メソッド単位の
共通ロジックを、1処理＝1行で一覧化する（1つの機能パッケージ内の複数画面から呼ばれるだけでは対象外）。

### 2.1 共通機能定義一覧

| No. | ID             | クラス／メソッド                                                                                                    | 機能名                      | 機能概要                                                                                                                                  | 処理概要                                                                                                   |
| --- | -------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1   | AZRCM001 | `PartialSQLGenerator`（`jp.co.kyocera.in.kok.sc_g.com.sql`）                                                    | 動的検索条件SQL生成         | 検索画面の入力値の数に応じて、WHERE句のSQL断片（LIKE前方一致／IN一覧一致、NULL安全版、決済先コードの現法/第三者判定）を動的に組み立てる。 | [AZRCM001 処理概要](<4-2_共通機能処理概要/[Sample]AZRCM001_PartialSQLGenerator_動的検索条件SQL生成.md>) |
| 2   | AZRCM002 | `DisplayMessageUtil`／`LogMessage`（`jp.co.kyocera.in.kok.sc_g.com.util`） `replaceSQL_I`／`replaceSQL_U` | 登録・更新SQL監査列自動付与 | 各画面Entityが組み立てたINSERT／UPDATE文に、監査列（CREATED/UPDATED_DATE・BY・PRG_NM、MODIFY_COUNT）を自動付与する。                      | [AZRCM002 処理概要](<4-2_共通機能処理概要/[Sample]AZRCM002_DisplayMessageUtil_監査列自動付与.md>)       |

### 2.2 使用マトリクス

| No. | ID             | 機能名                      | <span style="writing-mode: vertical-rl;">L001A</span> | <span style="writing-mode: vertical-rl;">L001B</span> | <span style="writing-mode: vertical-rl;">M001</span> | <span style="writing-mode: vertical-rl;">M002</span> | <span style="writing-mode: vertical-rl;">M003</span> | <span style="writing-mode: vertical-rl;">M004</span> | <span style="writing-mode: vertical-rl;">M005</span> | <span style="writing-mode: vertical-rl;">M006</span> | <span style="writing-mode: vertical-rl;">M007</span> | <span style="writing-mode: vertical-rl;">M008</span> | <span style="writing-mode: vertical-rl;">M009</span> | <span style="writing-mode: vertical-rl;">M990</span> | <span style="writing-mode: vertical-rl;">M999</span> | <span style="writing-mode: vertical-rl;">P001A</span> | <span style="writing-mode: vertical-rl;">P001B</span> | <span style="writing-mode: vertical-rl;">P001C</span> | <span style="writing-mode: vertical-rl;">P011A</span> | <span style="writing-mode: vertical-rl;">P011B</span> | <span style="writing-mode: vertical-rl;">P021A</span> | <span style="writing-mode: vertical-rl;">P021C</span> | <span style="writing-mode: vertical-rl;">S001A</span> | <span style="writing-mode: vertical-rl;">S001B</span> | <span style="writing-mode: vertical-rl;">S001C</span> | <span style="writing-mode: vertical-rl;">S001D</span> | <span style="writing-mode: vertical-rl;">S001E</span> | <span style="writing-mode: vertical-rl;">S001F</span> | <span style="writing-mode: vertical-rl;">S001G</span> | <span style="writing-mode: vertical-rl;">S001I</span> | <span style="writing-mode: vertical-rl;">S001J</span> | <span style="writing-mode: vertical-rl;">S011A</span> | <span style="writing-mode: vertical-rl;">S011B</span> | <span style="writing-mode: vertical-rl;">S011C</span> | <span style="writing-mode: vertical-rl;">S021A</span> | <span style="writing-mode: vertical-rl;">S021B</span> | <span style="writing-mode: vertical-rl;">S021C</span> | <span style="writing-mode: vertical-rl;">S021E</span> | <span style="writing-mode: vertical-rl;">S021F</span> | <span style="writing-mode: vertical-rl;">S021G</span> | <span style="writing-mode: vertical-rl;">S032A</span> |
| --- | -------------- | --------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| 1   | AZRCM001 | 動的検索条件SQL生成         |                                                       |                                                       |                                                      |                                                      |                                                      |                                                      | ●                                                   | ●                                                   |                                                      |                                                      |                                                      |                                                      |                                                      |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | ●                                                    | ●                                                    | ●                                                    |                                                       | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    |                                                       | ●                                                    | ●                                                    |
| 2   | AZRCM002 | 登録・更新SQL監査列自動付与 | ●                                                    |                                                       |                                                      |                                                      |                                                      |                                                      |                                                      |                                                      | ●                                                   |                                                      |                                                      | ●                                                   | ●                                                   | ●                                                    | ●                                                    | ●                                                    |                                                       |                                                       |                                                       | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    | ●                                                    |                                                       |                                                       | ●                                                    | ●                                                    | ●                                                    |                                                       |                                                       | ●                                                    |                                                       | ●                                                    | ●                                                    | ●                                                    | ●                                                    |                                                       |

## 3. 使用明細（検索用）

| 共通機能ID     | クラス／メソッド                   | 呼び出し元機能ID |
| -------------- | ---------------------------------- | ---------------- |
| AZRCM001 | `PartialSQLGenerator`            | M005             |
| AZRCM001 | `PartialSQLGenerator`            | M006             |
| AZRCM001 | `PartialSQLGenerator`            | P021C            |
| AZRCM001 | `PartialSQLGenerator`            | S001A            |
| AZRCM001 | `PartialSQLGenerator`            | S001B            |
| AZRCM001 | `PartialSQLGenerator`            | S001D            |
| AZRCM001 | `PartialSQLGenerator`            | S001E            |
| AZRCM001 | `PartialSQLGenerator`            | S001F            |
| AZRCM001 | `PartialSQLGenerator`            | S001G            |
| AZRCM001 | `PartialSQLGenerator`            | S001I            |
| AZRCM001 | `PartialSQLGenerator`            | S001J            |
| AZRCM001 | `PartialSQLGenerator`            | S011A            |
| AZRCM001 | `PartialSQLGenerator`            | S011B            |
| AZRCM001 | `PartialSQLGenerator`            | S011C            |
| AZRCM001 | `PartialSQLGenerator`            | S021A            |
| AZRCM001 | `PartialSQLGenerator`            | S021B            |
| AZRCM001 | `PartialSQLGenerator`            | S021C            |
| AZRCM001 | `PartialSQLGenerator`            | S021E            |
| AZRCM001 | `PartialSQLGenerator`            | S021G            |
| AZRCM001 | `PartialSQLGenerator`            | S032A            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | L001A            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | M007             |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | M990             |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | M999             |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | P001A            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | P001B            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | P001C            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | P021C            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001A            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001B            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001C            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001D            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001E            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001I            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S001J            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S011A            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S021A            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S021C            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S021E            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S021F            |
| AZRCM002 | `DisplayMessageUtil／LogMessage` | S021G            |

///

/// tab | 文書情報・改定履歴

## 文書情報

| 大分類 | 小分類 | ドキュメント名           | システムID | システム名       |
| ------ | ------ | ------------------------ | ---------- | ---------------- |
| 4      | 4.1    | 共通機能一覧（サンプル） | AZR        | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容                                                                                                                                                                                                                                                                                                               | 担当者 | 課題No./備考     |
| ------- | --------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------------- |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |

///
