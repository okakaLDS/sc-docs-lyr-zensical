---
title: "更新条件表"
tags:
  - 機能定義書
status: "作業中"
owner: "KCCS"
doc_no: "8.3.4"
---

# 更新条件表

対象プロシージャー: `NOUKI_PKG.NOUKI_RENKEI`。970行全体のソースコードを精読し、コメントアウトされた
無効ブロック（`(★切り替えで、処理停止)`等と明記された箇所）を除外したうえで、実際に実行される
UPDATE/INSERT/DELETE文を洗い出した結果。無効化されているテーブルの一覧は本ページ末尾の「5. 備考」を参照。

## 1. 基本情報

| 項目           | 内容                              |
| -------------- | ---------------------------------- |
| システムID     | AZR                                |
| DB(SQL)処理ID  | NOUKI_PKG                           |
| 作成日／作成者 | 不明（原設計書未受領のため未特定） |

## 2. 更新概要

スキーマ名とテーブル名は列を分けて記載する。更新種別は`INSERT`／`UPDATE`／`DELETE`／`MERGE`／`TRUNCATE`
を基本とするが、本オブジェクトでは「全件DELETE後にINSERTし直す洗い替え」を多用するため`DELETE→INSERT`
と表記している（Oracleの`MERGE`文・`TRUNCATE`文は本プロシージャーでは使用されていない）。

| 操作No. | 更新種別 | 接続先DB | スキーマ名 | テーブルID | テーブル名 | 契機（処理フェーズ） | 概要 | 備考 |
| ------- | -------- | -------- | ---------- | ---------- | ---------- | -------------------- | ---- | ---- |
| 1 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `CHUMON2` | 要確認（論理名未調査。役割はステージングテーブル） | プロシージャー開始時（前処理） | プロシージャー開始時に全件クリアし、`AZSDB0.TAZSD001`/`TAZSD002`等から当期間の対象データを再抽出 | 洗い替えパターン |
| 2 | UPDATE / DELETE | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `CHUMON2` | 要確認（論理名未調査。役割はステージングテーブル） | メイン処理中（カーソルループ中） | カーソルループ中、同一製伝No.・同一明細No.の重複行を検出した場合に、数量列を合算UPDATEしてから重複行をDELETE | 行圧縮（"行可変"）処理 |
| 3 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `NOUKI` | 要確認（論理名未調査。役割はステージングテーブル） | プロシージャー開始時（前処理、`CHUMON2`処理後） | プロシージャー開始時に全件クリアし、`AZSDB0.TAZSD003`から`CHUMON2`に該当する製伝No.分を再抽出 | 洗い替えパターン |
| 4 | UPDATE | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `CODE_MST` | 要確認（論理名未調査。共通設定マスターと推定） | 要確認 | 本処理の識別コード（`SHIKIBETSU_CD='A02', KEY1='00', KEY2='00'`）に該当する1件 | チェックポイント方式（次回実行時の差分抽出条件として参照される） |
| 5 | INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `RENKEI_RIREKI_LOG` | 要確認（論理名未調査。連携処理の実行履歴ログと推定） | 各連携ブロックの処理完了時 | 各連携ブロックの処理完了時 | 連携処理の実行履歴ログ |
| 6 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | SCSALES | `LYR03_NOUKI_TBL` | 要確認（論理名未調査。中間テーブル） | 中間テーブル洗い替え（前処理、`CHUMON2`／`NOUKI`準備後） | `LYR19.LYR03_NOUKI_TBL`（`LYR19.JCHZN_TBL`と結合）のうち、`predatetime`〜`todaytime`の更新分＋`CHUMON2`該当分を再構築 | `LYR19`→`SCSALES`方向の中間コピー（DBリンク`@LYR07`経由の旧方式から、`LYR19`スキーマ直読みへ移行済み） |
| 7 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | SCSALES | `ISD_HASSOU_TBL` | 要確認（論理名未調査。中間テーブル） | 中間テーブル洗い替え（前処理、上記6と同時） | `LYR19.ISD_HASSOU_TBL`（`LYR19.LYR03_TBL`／`JCHZN_TBL`と結合）のうち同上の対象分を再構築 | 同上 |
| 8 | UPDATE | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `CHUMON2` | 要確認（論理名未調査。役割はステージングテーブル） | メイン処理中（注文明細×納期データ紐付けループ内） | `SEIDEN_NO`／`NOUKI_START1`〜`4`／`NOUKI_MAX1`〜`4`を分納状況に応じて更新 | 分納消込ロジックの一部（[処理概要](NOUKI_PKG_02_処理概要.md)3.No.6参照） |
| 9 | UPDATE | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | 要確認（デフォルトスキーマ依存。配置スキーマSCSALESの可能性） | `NOUKI` | 要確認（論理名未調査。役割はステージングテーブル） | メイン処理中（`nouki_cur`ネストループ内） | 客先要求／営業希望／製造回答／客先回答の各納期数量を消込に応じて減算 | 分納消込ロジックの一部（同上） |
| 10 | INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | SCSALES | `SEIDEN_HAKKO_RIREKI` | 要確認（論理名未調査） | メイン処理中（E製伝かつ当日計上の場合のみ） | E製伝（区分01／02）で当日計上・数量非0の対象を1分納ごとに追加 | 発行履歴（E製伝限定） |
| 11 | DELETE→INSERT／INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | LYR19 | `LYR03_NOUKI_TBL` | 要確認（論理名未調査。最終連携先） | メインループ完了後（後処理、3パターン合成） | ①`SCSALES.LYR03_NOUKI_TBL`分／②`SCSALES.LYR03_NOUKI_TMP`分は該当`SEIDEN_NO`をDELETEしてから再INSERT。③`LYR19.LYR03_NOUKI_TMP`分はDELETEなしでINSERTのみ（追記型） | 全注→納期管理方向の最終的な連携先 |
| 12 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | LYR19 | `MEMO_TBL` | 要確認（論理名未調査） | メインループ完了後（後処理、E製伝型代納期連携） | `SCSALES.MEMO_TMP`該当`SEIDEN_NO`をDELETEしてから再INSERT |  |
| 13 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | LYR19 | `LYR03_NOUKI_LOG` | 要確認（論理名未調査） | メインループ完了後（後処理） | `SCSALES.LYR03_NOUKI_LOG`該当`SEIDEN_NO`をDELETEしてから再INSERT |  |
| 14 | DELETE→INSERT／INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | LYR19 | `ISD_HASSOU_TBL` | 要確認（論理名未調査。最終連携先） | メインループ完了後（後処理、3パターン合成） | ①`SCSALES.ISD_HASSOU_TBL`分／②`SCSALES.ISD_HASSOU_TMP`分は該当`SEIDEN_NO`をDELETEしてから再INSERT。③`LYR19.ISD_HASSOU_TMP`分はDELETEなしでINSERTのみ（追記型） |  |
| 15 | DELETE→INSERT | （記入：単一Oracleインスタンス内。DB名は原設計書未受領のため未特定） | LYR19 | `DSD_HASSOU_TBL` | 要確認（論理名未調査） | メインループ完了後（後処理） | `SCSALES.DSD_HASSOU_TMP`該当`SEIDEN_NO`をDELETEしてから再INSERT | ソース中に「`DSD_HASSOU_TBL`もこの対応はいる」との開発者コメントあり（`LYR19.DSD_HASSOU_TMP`からの追記型パターンが未実装の可能性、要確認） |

## 3. 更新条件・更新項目

画面設計書の更新条件表と同粒度（操作No.ごとに更新条件の条件式＋更新項目の全カラム）への詳細化は
**未実施**であり、今後の調査課題とする。現時点で特定できている範囲を操作No.単位で下表にまとめる。
「更新項目」の「全項目」は、対象テーブルの全カラムを洗い替えで再設定することを指す（省略表記ではない）。

| 操作No. | 更新条件 | 更新項目 |
| ------- | -------- | -------- |
| 1 | プロシージャー開始時に全件クリアし、`AZSDB0.TAZSD001`/`TAZSD002`等から当期間の対象データを再抽出 | 全項目 |
| 2 | カーソルループ中、同一製伝No.・同一明細No.の重複行を検出した場合に、数量列を合算UPDATEしてから重複行をDELETE | （記入：「ほか」による省略は不可のため全件列挙が必要。970行精読で特定済みのカラム名を全件記載すること — 未反映） |
| 3 | プロシージャー開始時に全件クリアし、`AZSDB0.TAZSD003`から`CHUMON2`に該当する製伝No.分を再抽出 | 全項目 |
| 4 | 本処理の識別コード（`SHIKIBETSU_CD='A02', KEY1='00', KEY2='00'`）に該当する1件 | 前回実行時刻（`CD1`列） |
| 5 | 各連携ブロックの処理完了時 | 実行時刻・処理内容メッセージ |
| 6 | `LYR19.LYR03_NOUKI_TBL`（`LYR19.JCHZN_TBL`と結合）のうち、`predatetime`〜`todaytime`の更新分＋`CHUMON2`該当分を再構築 | 全項目 |
| 7 | `LYR19.ISD_HASSOU_TBL`（`LYR19.LYR03_TBL`／`JCHZN_TBL`と結合）のうち同上の対象分を再構築 | 全項目 |
| 8 | `SEIDEN_NO`／`NOUKI_START1`〜`4`／`NOUKI_MAX1`〜`4`を分納状況に応じて更新 | `SEIDEN_NO`, `NOUKI_START1`〜`4`, `NOUKI_MAX1`〜`4` |
| 9 | 客先要求／営業希望／製造回答／客先回答の各納期数量を消込に応じて減算 | `KYAKUSAKI_YOKYU_SU`, `EIGYO_KIBO_SU`, `SEIZO_KAITO_SU`, `KYAKUSAKI_KAITO_SU` |
| 10 | E製伝（区分01／02）で当日計上・数量非0の対象を1分納ごとに追加 | 全項目 |
| 11 | ①`SCSALES.LYR03_NOUKI_TBL`分／②`SCSALES.LYR03_NOUKI_TMP`分は該当`SEIDEN_NO`をDELETEしてから再INSERT。③`LYR19.LYR03_NOUKI_TMP`分はDELETEなしでINSERTのみ（追記型） | 全項目 |
| 12 | `SCSALES.MEMO_TMP`該当`SEIDEN_NO`をDELETEしてから再INSERT | 全項目 |
| 13 | `SCSALES.LYR03_NOUKI_LOG`該当`SEIDEN_NO`をDELETEしてから再INSERT | 全項目 |
| 14 | ①`SCSALES.ISD_HASSOU_TBL`分／②`SCSALES.ISD_HASSOU_TMP`分は該当`SEIDEN_NO`をDELETEしてから再INSERT。③`LYR19.ISD_HASSOU_TMP`分はDELETEなしでINSERTのみ（追記型） | 全項目 |
| 15 | `SCSALES.DSD_HASSOU_TMP`該当`SEIDEN_NO`をDELETEしてから再INSERT | 全項目 |

## 4. トランザクション方針

| 項目                       | 内容 |
| -------------------------- | ---- |
| コミット単位               | ステージングテーブル（`CHUMON2`／`NOUKI`）の洗い替えごとに`COMMIT`（1トランザクション＝1ブロックではなく、ブロック単位でコミットする実装。[処理概要](NOUKI_PKG_02_処理概要.md)参照） |
| ロールバック範囲           | 未調査（要確認） |
| 異常終了時のデータ整合性   | 未調査（要確認） |
| 再実行時の重複登録防止キー | 未調査（要確認。`CHUMON2`／`NOUKI`等のステージングテーブルはDELETE→INSERTの洗い替えパターンだが、確定的な確認はできていない） |

## 5. 備考

**調査方法の訂正**：初版（Version 1.0時点）では正規表現によるテーブル名抽出のみを行い、コメント
アウトされたSQL文を除外できていなかった。今回、970行全体を精読し、行頭が`--`のブロック（無効化
されたSQL）を除外したうえで上記No.1〜15を再構成した。

**実際に実行される（生きている）テーブル**は上記No.1〜15のとおり：`CHUMON2`, `NOUKI`, `CODE_MST`,
`RENKEI_RIREKI_LOG`, `SCSALES.LYR03_NOUKI_TBL`, `SCSALES.ISD_HASSOU_TBL`,
`SCSALES.SEIDEN_HAKKO_RIREKI`, `LYR19.LYR03_NOUKI_TBL`, `LYR19.MEMO_TBL`, `LYR19.LYR03_NOUKI_LOG`,
`LYR19.ISD_HASSOU_TBL`, `LYR19.DSD_HASSOU_TBL`。このうち`SCSALES.*`／`LYR19.*`のテーブルは
ソース上でスキーマ接頭辞が明記されているため接続先スキーマは確定（要確認ではない）。`CHUMON2`／
`NOUKI`／`CODE_MST`／`RENKEI_RIREKI_LOG`のみ接頭辞なし（デフォルトスキーマ依存）で要確認。

なお、`LYR19.LYR03_NOUKI_TMP`／`LYR19.ISD_HASSOU_TMP`はDELETEのみ実行され、本プロシージャー内では
再INSERTされていない（他プロセスからの投入を前提としたワークテーブルの可能性、要確認）。

**コメントアウトされ、現在は実行されない（無効化された）テーブル**：`LYR19.LYR03_TBL`,
`LYR19.LYR03_TBL_LOG`, `LYR19.LYR03_MAIL_FLG_TBL`, `LYR19.ISD_HASSOU_LOG`, `LYR19.ONFLT_TBL`,
`LYR19.HASSOU_TBL`。いずれもソースコード中に`(★切り替えで、処理停止)`等のコメントがあり、
DBリンク`@LYR07`経由の旧方式から現行方式への切り替え時に無効化されたとみられる。設計書としては
現状「対象外」だが、切り戻しの可能性があるため削除はせず記録として残す。

`MEISAI_NOUKI`, `SCSALES.SEIDEN_NO_LIST`はテーブル名としてソース中に出現するが、参照箇所は
コメントアウトされた無効ブロックのみ（`INSERT INTO MEISAI_NOUKI`は全てコメント行）で、本プロシージャー
では実際に読み書きされていない。

No.6以降を含む全ての列マッピング（どのカラムがどの全注側カラムから来るか）の詳細な仕様化は、
上記の生存確認より深い精読が必要であり、今回の再調査でも対象外のまま。

---

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 8 | 8.3.4 | 更新条件表 | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |
