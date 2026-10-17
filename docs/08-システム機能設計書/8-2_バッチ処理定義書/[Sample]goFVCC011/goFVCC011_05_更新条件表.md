---
title: "更新条件表"
tags:
  - バッチ処理定義書
owner: "Rikkei"
doc_no: "8.2.6"
---

# 更新条件表

/// tab | 本文


## 1. 基本情報

| 項目       | 内容                       |
| ---------- | -------------------------- |
| システムID | LYR19                      |
| 処理ID     | goFVCC011                  |
| 作成日     | 2020-08-03（`FVCC011after_load.sql` Version 0.11 のヘッダーより） |
| 作成者     | SC Hirokazu-Kawabata（同上） |

## 2. 更新条件

| No. | 種別   | 接続先DB／スキーマ | テーブルID           | テーブル名             | 契機（処理フェーズ） | 更新内容                                     | 対象データ／条件                                             |
| --- | ------ | ------------------ | -------------------- | ---------------------- | -------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| 1   | UPDATE | LYR19              | `LYR03_UP_STATUS`    | 更新ステータス         | before_load          | `STATUS_FLG='1'`（取込中）に設定し、更新者・更新日時を退避する | `TABLE_MEI = 'CBB8'`                          |
| 2   | INSERT | LYR19              | `FVCC011`            | 未納実績データ         | SQL\*Loader          | 連携ファイルの明細レコードを追記（APPEND） | `RECORD_KBN <> '99'`                                         |
| 3   | INSERT | LYR19              | `SQLLDR_UPDATE_TMP`  | 取込件数一時           | SQL\*Loader          | 連携ファイルのトレーラレコードを追記       | `DATA_KBN = '99'`                                            |
| 4   | UPDATE | LYR19              | `LYR03_UP_STATUS`    | 更新ステータス         | after_load           | `STATUS_FLG='0'`（完了）に戻す             | `TABLE_MEI = 'CBB8'`                                         |
| 5   | INSERT | LYR19              | `SQLLDR_UPDATE_LOG`  | 取込履歴               | after_load           | 今回の取込件数情報を履歴として追記         | `SQLLDR_UPDATE_TMP.MAIL_CD = 'FVCC011'`                      |
| 6   | INSERT | LYR19              | `CB46`               | 未納処理データ         | after_load           | 未反映の未納データを差分反映               | `FVCC011.HAISHIN_BI > (SELECT NVL(MAX(HAISHIN_BI),'20100101') FROM CB46)` |
| 7   | UPDATE | LYR19              | `CB46`               | 未納処理データ         | after_load           | `KANREN_KAISHA_CD`を`FVCF006`から補完       | `CB46.HAISHIN_BI >= TO_CHAR(SYSDATE-50,'YYYYMMDD') AND KANREN_KAISHA_CD IS NULL` |
| 8   | UPDATE | LYR19              | `CB46`               | 未納処理データ         | after_load           | `KANREN_KAISHA_CD`を`FVCF303`から補完（No.7で埋まらなかった場合） | 同上 |
| 9   | DELETE | LYR19              | `SQLLDR_UPDATE`      | 取込状況               | after_load           | 最新世代より古い取込状況を削除             | `MAIL_CD='CBB8' AND CREATED_DATE < (SELECT MAX(CREATED_DATE) FROM SQLLDR_UPDATE WHERE MAIL_CD='CBB8' AND DATA_KBN='99' GROUP BY MAIL_CD)` |
| 10  | INSERT | LYR19              | `SQLLDR_UPDATE`      | 取込状況               | after_load           | 今回の取込件数情報を最新状況として登録     | `SQLLDR_UPDATE_TMP.MAIL_CD = 'FVCC011'`（`MAIL_CD`は`'CBB8'`固定で登録） |

上記No.1〜10のコミット後、ストアドプロシージャー`SP_MINOU_SYORI_2021`を実行する。プロシージャー内部の
DB更新内容は本表の対象外（`db-sql-processing-spec`側での作成有無は要確認）。旧バージョン
`SP_MINOU_SYORI_2019`の呼出し行は`rem`でコメントアウトされており現在は実行されない。

## 3. 更新カラム詳細

### No.6: `CB46`（未納処理データ）への差分INSERT

| 項目   | 内容                              |
| ------ | --------------------------------- |
| 登録元 | `FVCC011`（未納実績データ）       |

`INSERT`する95項目のうち、名称が異なる・固定値・後続処理で上書きされるものは下記No.1〜23の通り。
それ以外の72項目（No.24以降、本表では「上記以外」として集約）は`FVCC011`側の同名項目をそのまま設定する。

| No. | 項目名（`CB46`）              | 編集元（`FVCC011`）      | 編集方法／補足                                                              |
| --- | ------------------------------ | ------------------------- | ------------------------------------------------------------------------------ |
| 1   | `DATA_KBN`                     | `RECORD_KBN`              | 項目名が異なるため読み替え                                                    |
| 2   | `KANKATSU_JIGYOSHO_CD`         | —                         | `NULL`固定                                                                    |
| 3   | `KANREN_KAISHA_CD`             | `SHUUKEI_CD_MEISAI`       | 項目名が異なるため読み替え。後続のNo.7／No.8（`FVCF006`／`FVCF303`）で`NULL`の場合のみ上書き補完される |
| 4   | `IRAISAKI_JIGYOSHO_CD`         | `SEIZO_JIGYOSHO_CD`       | 項目名が異なるため読み替え                                                    |
| 5   | `IRAISAKI_KAKOBUMON_CD`        | `SEIZO_KAKOBUMON_CD`      | 項目名が異なるため読み替え                                                    |
| 6   | `ZEI_KBN`                      | —                         | `NULL`固定                                                                    |
| 7   | `KENKYU_KOSEN`                 | —                         | `NULL`固定                                                                    |
| 8   | `NOUHINSHO_NO`                 | `NOUHINSYO_NO`            | 表記ゆれ（`NOUHINSHO`／`NOUHINSYO`）のため読み替え                            |
| 9   | `NOUHINSYO_YOUSIKI_KBN`        | `NOUHINSYO_YOSHIKI_KBN`   | 表記ゆれ（`YOUSIKI`／`YOSHIKI`）のため読み替え                                |
| 10  | `KC_KEIYAKU_TANKA_GAI`         | `KEIYAKU_TANKA_GAI`       | 項目名が異なるため読み替え                                                    |
| 11  | `KC_KEIYAKU_KATADAI_GAI`       | `KEIYAKU_KATADAI_GAI`     | 項目名が異なるため読み替え                                                    |
| 12  | `ADDER_KBN_1`                  | `KEISANSHIKI_KBN_1`       | 項目名が異なるため読み替え                                                    |
| 13  | `ADDER_KBN_2`                  | `KEISANSHIKI_KBN_2`       | 項目名が異なるため読み替え                                                    |
| 14  | `MINOU_ZANSU`                  | —                         | `NULL`固定。更新契機は本ソース範囲内には無く未確認。（記入：別ソース〈画面設計書側等〉での更新有無を確認要） |
| 15  | `HENKOBI`                      | `HAISHIN_BI`              | 項目名が異なるため読み替え（配信日を変更日として設定）                        |
| 16  | `SENRYAKU_BUSSHI_KBN`          | —                         | `NULL`固定                                                                    |
| 17  | `SENRYAKU_BUSSHI_TORIHIKI_KBN` | —                         | `NULL`固定                                                                    |
| 18  | `ZEIKOMI_KEIYAKU_TANKA`        | —                         | `NULL`固定                                                                    |
| 19  | `ZEIKOMI_KATADAI`              | —                         | `NULL`固定                                                                    |
| 20  | `EIGYO_KANRI_CD`               | —                         | `NULL`固定                                                                    |
| 21  | `URIAGE_KINGAKU`               | `KEIYAKU_KINGAKU_NAI`     | 項目名が異なるため読み替え                                                    |
| 22  | `EIGYO_JIGYOUBU_CD`            | `EIGYO_JIGYOBU_CD`        | 表記ゆれ（`JIGYOU`／`JIGYO`）のため読み替え                                   |
| 23  | `SEIZO_JIGYOUBU_CD`            | `SEIZO_JIGYOBU_CD`        | 表記ゆれ（`JIGYOU`／`JIGYO`）のため読み替え                                   |
| 24  | 上記以外（72項目）             | 同名項目                  | 変換なしでそのまま設定                                                        |

*No.1〜23とNo.24の対応関係は`FVCC011after_load.sql`の`INSERT INTO CB46 (...) SELECT ... FROM FVCC011`の
INSERT列リストとSELECT列リストを1対1で突き合わせて特定したもの（両リストとも95項目）。*

### No.1／No.4: `LYR03_UP_STATUS`（更新ステータス）のUPDATE

| No. | カラム名       | 論理名     | 編集元       | 編集方法／補足                                          |
| --- | -------------- | ---------- | ------------ | ------------------------------------------------------- |
| 1   | `STATUS_FLG`   | ステータス | —            | before_loadで`'1'`、after_loadで`'0'`を設定             |
| 2   | `LASTED_DATE`  | 前回日時   | `CREATED_DATE` | before_loadのみ。前回の作成日時を退避する             |
| 3   | `LASTED_BY`    | 前回更新者 | `CREATED_BY` | before_loadのみ。前回の作成者を退避する                 |
| 4   | `CREATED_DATE` | 作成日時   | —            | before_loadのみ。`sysdate`                              |
| 5   | `CREATED_BY`   | 作成者     | —            | before_loadのみ。`'SQLLDR'`固定                         |

## 4. トランザクション方針

| 項目                       | 内容                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| コミット単位               | `FVCC011before_load.sql`／`FVCC011after_load.sql`はそれぞれSQL\*Plusスクリプト単位。after_load内では`CB46`関連の全更新（No.6〜10）までを1トランザクションとし、末尾で`COMMIT`する。SQL\*Loaderは`ROWS=1000`／`DIRECT=TRUE`のため1000行ごとにコミットされる |
| ロールバック範囲           | after_load内の`COMMIT`より前に発生したエラーはSQL\*Plusの既定動作でロールバックされる。SQL\*Loaderで既にロード済みの`FVCC011`のデータは**ロールバックされない** |
| 異常終了時のデータ整合性   | `LYR03_UP_STATUS.STATUS_FLG`が`'1'`（取込中）のまま残留しうる。`FVCC011`にロード済みだが`CB46`未反映という中間状態も発生しうる |
| 再実行時の重複登録防止キー | `CB46`は`HAISHIN_BI`（配信日）が`CB46`の最大値より大きいレコードのみを対象とすることで重複反映を防いでいる。`FVCC011`自体はAPPENDのため同一世代を再ロードすると重複する（呼出元`COMM_ftp.bat`の世代重複チェックで防止。詳細は[COMM_ftp](<../[Sample]COMM_ftp/index.md>)参照） |

///

/// tab | 文書情報・改定履歴

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 8 | 8.2.6 | 更新条件表 | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |

///
