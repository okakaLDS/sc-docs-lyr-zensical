---
title: "AZRCM001 — PartialSQLGenerator（動的検索条件SQL生成）"
tags:
  - 共通機能
status: "作業中"
owner: "KCCS"
doc_no: "4.2"
---

# AZRCM001 — PartialSQLGenerator（動的検索条件SQL生成）

## 1. 共通機能

| 共通機能ID | 機能名                     |
| ---------- | ---------------------------- |
| AZRCM001 | 動的検索条件SQL生成          |

クラスは`jp.co.kyocera.in.kok.sc_g.com.sql.PartialSQLGenerator`（`static`メソッドのみを持ち、
インスタンスの状態を保持しないユーティリティクラス）。

## 2. 処理概要

検索画面のEntityクラス（DBアクセス層）が、ユーザーが実際に入力・選択した検索条件の数に応じて、
WHERE句のSQL断片を動的に組み立てるための共通ユーティリティ。多値選択（営業所コードの複数選択など）に
対応する可変個数の`?`プレースホルダを持つSQL文字列を、呼び出し元が用意した検索対象カラム名・繰り返し数
・「WHERE句の先頭条件かどうか」から組み立てて返す。

### 2.1 処理の流れ

呼び出し元Entityは、検索条件1つにつき以下の手順で本クラスのメソッドを1回呼び出す
（検索条件が複数ある場合は条件の数だけ繰り返す）。

① 呼び出し元が、検索対象カラム名・値（複数値の場合は配列）・「WHERE句の先頭条件か否か」を
   引数として渡し、条件の性質に応じたメソッド（下記2.2）を1つ選んで呼び出す。

② メソッド内部で値の有無を判定する。
   - 値が空／未入力の場合：条件式を生成せず空文字列（または`1=1`、メソッドにより異なる）を返す。
   - 値がある場合：値の個数（単一／複数）に応じて`?`プレースホルダの個数を決定し、
     複数値なら`OR`（LIKE系）または`IN (...)`（IN系）で連結する。

③ 生成したSQL断片を呼び出し元へ返す。呼び出し元はこれをWHERE句へ連結し、続けて
   プレースホルダの数だけ`PreparedStatement`へ値をバインドする。

※ 本クラス自身はSQLを実行しない。文字列を組み立てて返すだけであり、実行は常に呼び出し元Entityの
   責務である。

### 2.2 対象クラス／メソッド

- `jp.co.kyocera.in.kok.sc_g.com.sql.PartialSQLGenerator`（`static`メソッドのみ、状態を持たないユーティリティクラス）
    - `createPartialSql_like(...)` … 前方一致（`LIKE ? \|\| '%'`）条件。複数値選択時はOR連結して繰り返す
    - `createPartialSql_like_dynamic(...)` … `like`と同じだが`SqlFormat.formatDyncond`を使わないEntity向け（空値時は`1=1`を返す）
    - `createPartialSql_like_nvl(...)` … 前方一致 + `NVL(col, '固定文字列')`でNULLを既定値扱いにする版
    - `createPartialSql_like_nvl2(...)` … 前方一致 + `NVL(col, 別カラム)`でNULL時に別カラムへフォールバックする版
    - `createPartialSql_dynamic(...)` … 値が空でない場合のみ`AND col = ?`を追加（最も単純な条件付与）
    - `createPartialSql_in(...)` … 完全一致（`col = ?`）または複数値の`IN (?, ?, ...)`条件
    - `createPartialSql_in_nvl(...)` … `in`と同じだが`NVL(col, '固定文字列')`でNULLを既定値扱いにする版
    - `createGenpouCheck(kbn, table, col)` … 本クラス内で唯一、汎用SQL整形ではなく具体的な業務ルールを
      持つメソッド。詳細・注意事項は下記2.3参照

### 2.3 業務ルール・注意事項

- **制約**：`createGenpouCheck`は「現法/第三者区分」（`kbn`＝1:現法、2:第三者）に応じて、対象テーブルの
  決済先コード（`KESSAISAKI_CD`）が共通コードマスター（`SCSALES.CODE_MST`、識別コード`L01`）に登録されて
  いるかを`EXISTS`／`NOT EXISTS`で判定する条件式を生成する。テーブル名・カラム名は呼び出し前にホワイト
  リスト（現状`JCHZN_TBL`／`KESSAISAKI_CD`のみ）と照合し、一致しない場合は`IllegalArgumentException`を
  送出する（SQLインジェクション対策を兼ねた簡易ガード）。現時点でこのメソッドを実際に呼び出している
  のは`S021G`（U31＝売上予定管理）のみ。
- **排他制御**：本関数群はSQL文字列を組み立てるだけで、コミット／ロールバックの制御は一切行わない
  （呼び出し元のEntity/Controlクラス側の責務）。

### 2.4 対象項目

該当なし（本機能は項目単位で対象／非対象が分かれる性質のものではなく、呼び出し元が渡した任意の
カラムに対してSQL断片を組み立てるユーティリティであるため）。

### 2.5 参照ドキュメント

該当なし（本ページで完結する）。

## 3. 対象画面・ボタン・項目

呼び出し元は以下の20機能。いずれも各機能のEntityクラス内、検索処理の`read`系メソッドから呼ばれる。
特定のボタン押下ではなく、各画面の「検索」実行時（一覧表示の初回表示／再検索）に呼び出される。

| 機能ID | ファイル |
| ------ | ---------------------------- |
| M005   | `lyr07_SR01Entity.java`      |
| M006   | `lyr07_SJ01Entity.java`      |
| P021C  | `lyr07_JS01Entity.java`      |
| S001A  | `lyr07_C11Entity.java`       |
| S001B  | `lyr07_S11Entity.java`       |
| S001D  | `lyr07_I21Entity.java`       |
| S001E  | `lyr07_I21DEntity.java`      |
| S001F  | `lyr07_I21DLEntity.java`     |
| S001G  | `lyr07_E21Entity.java`       |
| S001I  | `lyr07_PI21Entity.java`      |
| S001J  | `lyr07_PI21DEntity.java`     |
| S011A  | `lyr07_K11Entity.java`       |
| S011B  | `lyr07_F11Entity.java`       |
| S011C  | `lyr07_SR0AEntity.java`      |
| S021A  | `lyr07_U11Entity.java`       |
| S021B  | `lyr07_U21Entity.java`       |
| S021C  | `lyr07_J01Entity.java`       |
| S021E  | `lyr07_J91AEntity.java`      |
| S021G  | `lyr07_U31Entity.java`       |
| S032A  | `lyr07_M32Entity.java`       |

## 4. 更新仕様（対象テーブル）

該当なし（本関数群はWHERE句のSQL文字列を組み立てて返すのみで、DBへの読み書きは呼び出し元のEntity
クラス自身が実行する。唯一の例外`createGenpouCheck`も、`EXISTS`/`NOT EXISTS`のサブクエリ文字列を
構築して返すだけで、自らSQLを実行するわけではない）。

## 5. 更新条件表

| 共通機能ID | 対象テーブル |
| ---------- | -------------- |
| AZRCM001 | 該当なし（DBを更新しない参照系SQL断片生成のため） |

| No. | 項目名 | キー | UPDATE | キー | INSERT | キー | DELETE |
| --- | -------- | ---- | -------- | ---- | -------- | ---- | -------- |
| 該当なし |        |      |          |      |          |      |          |

---

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 4 | 4.2 | 共通機能処理概要 | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |
