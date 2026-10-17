---
title: "インターフェース仕様"
tags:
  - 機能定義書
owner: "KCCS"
doc_no: "8.3.2"
---

# インターフェース仕様

/// tab | 本文


## 1. 基本情報

| 項目           | 内容                              |
| -------------- | ---------------------------------- |
| システムID     | AZR                                |
| DB(SQL)処理ID  | NOUKI_PKG                          |
| オブジェクト名 | `NOUKI_PKG.NOUKI_RENKEI`           |
| 作成日／作成者 | 不明（原設計書未受領のため未特定） |

## 2. トリガー発火条件（オブジェクト種別がTRIGGERの場合のみ作成）

該当なし（本オブジェクトはPROCEDUREのため対象外）。

## 3. 引数定義

| No. | プロシージャー／ファンクション名 | 引数名 | IN/OUT/INOUT | 型 | 桁数 | 必須 | 説明 |
| --- | ------------------------------ | -------- | -------------- | ---- | ------ | ------ | ------ |
| 1 | `NOUKI_RENKEI` | 該当なし（引数を1つも取らないプロシージャー。`PROCEDURE NOUKI_RENKEI IS` と宣言され、呼び出し側は`EXECUTE NOUKI_PKG.NOUKI_RENKEI;`のみ） | － | － | － | － | － |

## 4. 戻り値（FUNCTIONの場合）

| No. | プロシージャー／ファンクション名 | 型 | 桁数 | 戻り値の意味 | 異常時の戻り値 |
| --- | ------------------------------ | ---- | ---- | ------------ | -------------- |
| － | 該当なし（本パッケージにFUNCTIONは存在せず、`NOUKI_RENKEI`はPROCEDUREのため戻り値なし） | － | － | － | － |

## 5. 例外（EXCEPTION）定義

該当なし。`NOUKI_RENKEI`プロシージャーの本体（PACKAGE BODY 36〜1001行）を全文確認したが、
トップレベル・ネストとも`EXCEPTION`ブロックは1つも存在しない（`NO_DATA_FOUND`等の捕捉処理は
同パッケージ内の別プロシージャー`UPDATE_NOUKI_TO_NOUKI`／`UPDATE_NOUKI_TO_NOUKI_KAIGAI`／
`UPDATE_NOUKI_TO_ZENCHU`にあり、本プロシージャーのものではない）。

本プロシージャーは呼び出し元（バッチ`NOUKI_RENKEI.sql`）側で`WHENEVER SQLERROR EXIT SQL.SQLCODE`／
`WHENEVER OSERROR EXIT FAILURE`を設定しており、未捕捉のOracleエラーが発生した場合はSQL\*Plus自体が
非0の終了コードで異常終了する（[処理概要](NOUKI_PKG_02_処理概要.md)5.も参照）。

## 6. パッケージ内の他プロシージャーの引数（参考、未詳細調査）

| プロシージャー名               | 引数                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------ |
| `NOUKI_RENKEI_MANUAL`           | なし（`PACKAGE.sql`宣言部で確認済み）                                                             |
| `UPDATE_NOUKI_TO_NOUKI`         | `seidenNo IN VARCHAR2, chumonNo IN VARCHAR2, meisaiNo IN VARCHAR2, updatedDt IN DATE, forceFlag IN NUMBER`（全てIN、OUTなし） |
| `UPDATE_NOUKI_TO_NOUKI_KAIGAI`  | `seidenNo IN VARCHAR2, saSuryo IN NUMBER, denpyoKbn IN VARCHAR2, updatedDt IN DATE, forceFlag IN NUMBER`（全てIN、OUTなし。`PACKAGE.sql`宣言部で確認済み） |
| `UPDATE_NOUKI_TO_ZENCHU`        | `forceFlag IN NUMBER`                                                                            |

///

/// tab | 文書情報・改定履歴

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 8 | 8.3.2 | インターフェース仕様 | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |

///
