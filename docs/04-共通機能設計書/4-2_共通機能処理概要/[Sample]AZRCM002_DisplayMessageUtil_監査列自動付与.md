---
title: "AZRCM002 — DisplayMessageUtil／LogMessage（登録・更新SQL監査列自動付与）"
tags:
  - 共通機能
status: "作業中"
owner: "KCCS"
doc_no: "4.2"
---

# AZRCM002 — DisplayMessageUtil／LogMessage（登録・更新SQL監査列自動付与）

/// tab | 本文


## 1. 共通機能

| 共通機能ID | 機能名                             |
| ---------- | ------------------------------------- |
| AZRCM002 | 登録・更新SQL監査列自動付与           |

実クラスは2段構成。呼び出し窓口が`jp.co.kyocera.in.kok.sc_g.com.util.DisplayMessageUtil`
（各画面Entityが`new DisplayMessageUtil()`で保持するインスタンス）、実際の文字列加工ロジックを持つのが
`jp.co.kyocera.in.kok.sc_g.com.util.LogMessage`（`DisplayMessageUtil`が内部で処理を委譲する先）。
`DisplayMessageUtil`はメッセージリソース取得（`getMessage`／`getIDMsg`）ももう一つの役割として持つが、
本機能の対象は`replaceSQL_I`／`replaceSQL_U`の2メソッドのみとする。

## 2. 処理概要

各画面のEntityクラスが自前で組み立てたINSERT文／UPDATE文の文字列（テーブル名・業務カラムのみ）を、
実行直前に本機能へ渡すと、監査列（作成日時／作成者／更新日時／更新者／プログラム名／編集回数）の
プレースホルダを自動的に追記した完成形のSQL文字列を返す、DB書き込み直前に必ず経由する共通処理。

### 2.1 処理の流れ

① 呼び出し元Entityが、テーブル名・業務カラムのみを含むINSERT文／UPDATE文の文字列を自前で組み立てる。

② 実行直前に、その文字列を`replaceSQL_I`（INSERT用）または`replaceSQL_U`（UPDATE用）へ渡す。
   - `replaceSQL_I(String sSQL)`：`INSERT INTO tbl (cols) VALUES (vals)`の`VALUES`
     （`" VALUES"`／`"\tVALUES"`の2表記に対応）を文字列検索で見つけ、カラム列側に
     `CREATED_DATE, CREATED_BY, CREATED_PRG_NM, UPDATED_DATE, UPDATED_BY, UPDATED_PRG_NM, MODIFY_COUNT,`
     を、値側に対応する`?`プレースホルダ（日時は`NVL(TO_DATE(?,'YYYY/MM/DD HH24:MI:SS'),sysdate)`、
     編集回数は初期値の固定値）を差し込む。どちらの`VALUES`表記も見つからない場合は
     `FoundationException`を送出する。
   - `replaceSQL_U(String sSQL)`：`UPDATE ... SET ...`の`SET`
     （`" SET "`／`"\tSET\t"`／`"\tSET "`／`" SET\t"`の4表記に対応）を見つけ、直後に
     `UPDATED_DATE = NVL(TO_DATE(?,...),sysdate), UPDATED_BY = ?, UPDATED_PRG_NM = ?, MODIFY_COUNT = decode(greatest(MODIFY_COUNT,MAX-1),MAX-1,MIN,MODIFY_COUNT+1),`
     を差し込む。`SET`が見つからない場合は`FoundationException`を送出する。

③ 呼び出し元は返された完成SQLで`conn.prepareStatement(...)`を実行し、戻り値の`?`の数だけ追加で
   `setString(...)`をバインドしてから`stmt.executeUpdate()`する。本機能自身はSQL文字列を加工して
   返すのみで、DBへの読み書きは一切行わない。

**呼び出し例**（`M007/lyr07_LM01Entity.java` `create()`を要約）：

```java
if ("Oracle".equals(conn.getMetaData().getDatabaseProductName())) {
    stmt = conn.prepareStatement(objMessage.replaceSQL_I(m_inscmd));
} else if (... MSSQL ...) {
    stmt = conn.prepareStatement(objMessage.replaceSQL_I_MSSQL(m_inscmd)); // 下記2.3「既知の不具合」参照：未実装
}
...
setString(1, data.getsSysdate(),    stmt); // CREATED_DATE
setString(2, data.getsUser_ID(),    stmt); // CREATED_BY
setString(3, m_sCreateProgramName,  stmt); // CREATED_PRG_NM
setString(4, data.getsSysdate(),    stmt); // UPDATED_DATE
setString(5, data.getsUser_ID(),    stmt); // UPDATED_BY
setString(6, m_sCreateProgramName,  stmt); // UPDATED_PRG_NM
setString(7, data.getSEIDEN_NO(),   stmt); // ここから業務カラム
...
return stmt.executeUpdate();
```

### 2.2 対象クラス／メソッド

実クラスは2段構成。

- `jp.co.kyocera.in.kok.sc_g.com.util.DisplayMessageUtil`（呼び出し窓口。各画面Entityが
  `new DisplayMessageUtil()`で保持するインスタンス）
    - `replaceSQL_I(String sSQL)` … INSERT文へ監査列を差し込む
    - `replaceSQL_U(String sSQL)` … UPDATE文へ監査列を差し込む
    - `getMessage(...)`／`getIDMsg(...)` … メッセージリソース取得。本機能とは別の役割のため対象外
- `jp.co.kyocera.in.kok.sc_g.com.util.LogMessage`（`DisplayMessageUtil`が内部で処理を委譲する先。
  実際の文字列加工ロジックを持つ）
    - `getModify_Count_Min()`／`getModify_Count_Max()` … `MODIFY_COUNT`の折り返し境界値取得（2.3参照）

### 2.3 業務ルール・注意事項

- MODIFY_COUNT（編集回数）の折り返しルール：
  `decode(greatest(MODIFY_COUNT,MAX-1),MAX-1,MIN,MODIFY_COUNT+1)` は「現在値が既に`MAX-1`以上に
  達していれば`MIN`へ巻き戻し、そうでなければ+1する」という意味。上限に達しても異常終了・桁溢れさせず、
  設定された範囲内でカウンタを循環させる楽観ロック用カウンタである。`MIN`／`MAX`は固定値ではなく、
  `LogMessage.getModify_Count_Min()`／`getModify_Count_Max()`が実行時に取得する設定値：
    - オンライン処理時：`CoreTools.getContainer().getString("delimansys.modify_count.min/.max")`
    - バッチ処理時（`CoreTools.isBatch()`）：`CoreTools.getBatchProp()`から同名キー
    - 設定が無い場合は`MIN`＝`"0"`、`MAX`＝`Integer.MAX_VALUE`にフォールバックする。
  - 排他制御について：本カウンタ自体は楽観ロック用の編集回数であり、その比較・利用
    （`SELECT...FOR UPDATE`等の明示的排他機構を伴うか否かを含む）は呼び出し元Entity側の実装次第
    （本機能自体は値を巻き戻し計算して返すのみ）。
- 既知の不具合（未実装スタブ）：`replaceSQL_I_MSSQL`／`_PGSQL`／`_MYSQL`／`_DB2`と
  `replaceSQL_U_MSSQL`／`_PGSQL`／`_MYSQL`／`_DB2`は全て`// TODO 自動生成されたメソッド・スタブ`の
  コメントのまま`return null;`のみで未実装。呼び出し元21機能は全て
  `conn.getMetaData().getDatabaseProductName()`で分岐し、Oracle以外のDB製品名だった場合は
  この未実装メソッドを呼んで`conn.prepareStatement(null)`を実行することになる（本番はOracle固定運用
  のため顕在化していないが、DB移行時などにOracle以外へ接続した場合は即座に例外となる潜在バグ）。
- 単純な文字列検索によるパースの限界：`SET`／`VALUES`の位置特定は正規のSQLパーサではなく
  `indexOf`ベースの文字列検索（4種・2種のキーワード表記ゆれを吸収するのみ）。SQL文字列中に
  サブクエリや文字列リテラルとして偶然`" SET "`／`" VALUES"`が先に出現するSQLを渡した場合、
  誤った位置に監査列を差し込む可能性がある（現状の呼び出し元21機能のSQLでは顕在化していないが、
  新規にこの機能を呼び出すSQLを追加する際は先頭側に`SET`／`VALUES`が1回だけ出現する単純な構文に
  留めること）。
- `replaceSQL_I`／`replaceSQL_U`は監査列付与の窓口が1つに統一されているのみで、監査列を書くかどうか
  の判断自体は行わない：呼び出すかどうかは各画面のEntityクラス側の実装次第であり、本機能を経由しない
  独自SQL（本機能を経由せず監査列を自前で付与、または未付与）が存在する可能性がある。

### 2.4 対象項目

該当なし（本機能は特定の業務項目を対象とするものではなく、呼び出し元が指定した任意のテーブルへの
INSERT／UPDATE文に対して監査列を横断的に追記するユーティリティであるため。対象となる監査列自体は
「4. 更新仕様（対象テーブル）」に一覧化する）。

### 2.5 参照ドキュメント

該当なし（本ページで完結する）。

## 3. 対象画面・ボタン・項目

特定のボタン押下ではなく、**各機能のEntityクラスにおける`create`／`update`系メソッド内、
`PreparedStatement`実行直前**に必ず経由する。呼び出し元は21機能・172呼び出し箇所：

| 機能ID | Entityファイル |
| -------------- | ------------------------------ |
| L001A          | `lyr07_LG1Entity.java`         |
| M007           | `lyr07_LM01Entity.java`        |
| M990           | `lyr07_SUM01Entity.java`       |
| M999           | `lyr07_M91Entity.java`         |
| P001A          | `lyr07_C01Entity.java`         |
| P001B          | `lyr07_S01Entity.java`         |
| P001C          | `lyr07_L01Entity.java`         |
| P021C          | `lyr07_JS01Entity.java`        |
| S001A          | `lyr07_C11Entity.java`         |
| S001B          | `lyr07_S11Entity.java`         |
| S001C          | `lyr07_L11Entity.java`         |
| S001D          | `lyr07_I21Entity.java`         |
| S001E          | `lyr07_I21DEntity.java`        |
| S001I          | `lyr07_PI21Entity.java`        |
| S001J          | `lyr07_PI21DEntity.java`       |
| S011A          | `lyr07_K11Entity.java`         |
| S021A          | `lyr07_U11Entity.java`         |
| S021C          | `lyr07_J01Entity.java`         |
| S021E          | `lyr07_J91AEntity.java`        |
| S021F          | `lyr07_AF010Entity.java`       |
| S021G          | `lyr07_U31Entity.java`         |

各機能とも、`replaceSQL_I`はその機能が持つ`create`（新規登録）系メソッド内、`replaceSQL_U`は
`update`（更新）系メソッド内で呼ばれる（1機能に複数の対象テーブルがある場合はテーブルの数だけ
ペアで呼ばれる。例：P001B/S01Entityは18箇所＝9テーブル×INSERT/UPDATE）。

## 4. 更新仕様（対象テーブル）

本機能は特定の1テーブルを対象とするものではなく、**呼び出し元が指定した任意のテーブルへのINSERT／
UPDATE文に対して、以下の監査列を横断的に追記する**（対象テーブル名・業務カラムは呼び出し元が
そのつど渡すSQL文字列に依存するため、本機能自身は対象テーブルを限定しない。テーブルごとの章内細分化は
行わない）。

| No. | 項目名           | INSERT時に設定する値                                              | UPDATE時に設定する値                                              |
| --- | ------------------ | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1   | CREATED_DATE       | `NVL(TO_DATE(?,'YYYY/MM/DD HH24:MI:SS'),sysdate)`（呼び出し元がバインドする日時、通常は処理時点のシステム日時） | （対象外・UPDATEでは変更しない）                                      |
| 2   | CREATED_BY         | 呼び出し元がバインドするユーザーID                                    | （対象外）                                                            |
| 3   | CREATED_PRG_NM     | 呼び出し元がバインドするプログラム名                                  | （対象外）                                                            |
| 4   | UPDATED_DATE       | CREATED_DATEと同じ値（新規登録時は作成＝更新扱い）                    | `NVL(TO_DATE(?,...),sysdate)`（呼び出し元がバインドする更新時点の日時） |
| 5   | UPDATED_BY         | CREATED_BYと同じ値                                                    | 呼び出し元がバインドするユーザーID                                    |
| 6   | UPDATED_PRG_NM     | CREATED_PRG_NMと同じ値                                                | 呼び出し元がバインドするプログラム名                                  |
| 7   | MODIFY_COUNT       | `MIN`固定値（`getModify_Count_Min()`で取得、既定`"0"`）               | `decode(greatest(MODIFY_COUNT,MAX-1),MAX-1,MIN,MODIFY_COUNT+1)`（現在値からの折り返し増分。詳細は「2. 処理概要」の業務ルール） |

## 5. 更新条件表

| 共通機能ID | 対象テーブル |
| ---------- | -------------- |
| AZRCM002 | 呼び出し元が指定する任意のテーブル（本機能自体は対象テーブルを限定しない。詳細は「4. 更新仕様」） |

| No. | 項目名        | キー | UPDATE                                            | キー | INSERT                                     | キー | DELETE |
| --- | --------------- | ---- | ---------------------------------------------------- | ---- | --------------------------------------------- | ---- | -------- |
| 1   | UPDATED_DATE    | -    | 呼び出し元バインドの日時（`SET`検出時に必ず追加）    | -    | CREATED_DATEと同値で追加                       | -    | 該当なし |
| 2   | UPDATED_BY      | -    | 呼び出し元バインドのユーザーID                        | -    | CREATED_BYと同値で追加                         | -    | 該当なし |
| 3   | UPDATED_PRG_NM  | -    | 呼び出し元バインドのプログラム名                      | -    | CREATED_PRG_NMと同値で追加                     | -    | 該当なし |
| 4   | MODIFY_COUNT    | -    | `decode(greatest(MODIFY_COUNT,MAX-1),MAX-1,MIN,MODIFY_COUNT+1)`（※1） | -    | `MIN`固定値（※1）                              | -    | 該当なし |
| 5   | CREATED_DATE    | -    | 対象外（UPDATEでは変更しない）                        | -    | 呼び出し元バインドの日時                        | -    | 該当なし |
| 6   | CREATED_BY      | -    | 対象外                                                | -    | 呼び出し元バインドのユーザーID                  | -    | 該当なし |
| 7   | CREATED_PRG_NM  | -    | 対象外                                                | -    | 呼び出し元バインドのプログラム名                | -    | 該当なし |

※1　`MIN`／`MAX`は環境ごとの設定値（`delimansys.modify_count.min`／`.max`、オンライン時は
コンテナ設定・バッチ時はバッチプロパティから取得、未設定時は`MIN="0"`／`MAX=Integer.MAX_VALUE`）。

本機能はDELETE文には一切関与しない（`replaceSQL_I`／`replaceSQL_U`の2メソッドのみで、DELETE用の
メソッドはソースコード上に存在しない）。

///

/// tab | 文書情報・改定履歴

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 4 | 4.2 | 共通機能処理概要 | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |

///
