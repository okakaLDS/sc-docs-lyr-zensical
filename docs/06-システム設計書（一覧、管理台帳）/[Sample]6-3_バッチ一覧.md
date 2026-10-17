---
title: "バッチ一覧"
tags:
  - 管理台帳
owner: "KCCS"
doc_no: "6.3"
---
# バッチ一覧

/// tab | 本文


## 1. バッチ一覧

| No. | バッチ分類 | バッチファイル名 | 処理概要 | 参照エンジン | 備考 |
| --- | --- | --- | --- | --- | --- |
| 1 | - | NOUKI_RENKEI | 全注_納期データ連携。`NOUKI_PKG.NOUKI_RENKEI`（[DB(SQL)処理定義書](<../08-システム機能設計書/8-3_DB(SQL)処理定義書/[Sample]NOUKI_PKG/index.md>)）を呼ぶ薄いラッパー。 | | |
| 2 | FTP Flow | FVAAD13 | 出荷指示・KCAF連携データ取込。 | COMM_ftp（推定。要確認：FVCC007のみソース確認済み） | |
| 3 | FTP Flow | FVCC007 | CB41/CBB5連携データ取込。 | COMM_ftp（ソース確認済） | |
| 4 | FTP Flow | FVCC008 | CB42連携データ取込。 | COMM_ftp（推定。要確認） | |
| 5 | FTP Flow | FVCC009 | 生産実績（CB52）連携データ取込。 | COMM_ftp（推定。要確認） | |
| 6 | FTP Flow | FVCC010 | CB45連携データ取込。 | COMM_ftp（推定。要確認） | |
| 7 | FTP Flow | FVCC011 | CB46連携データ取込（未納処理連携）。 | COMM_ftp（ソース確認済） | |
| 8 | FTP Flow | FVCC014 | CB0F連携データ取込。 | COMM_ftp（推定。要確認） | |
| 9 | FTP Flow | FVCC015 | CBD5連携データ取込。 | COMM_ftp（推定。要確認） | |
| 10 | FTP Flow | FVCF006 | 受注残・分納情報取込。 | COMM_ftp（推定。要確認） | |
| 11 | FTP Flow | FVCF303 | 受注残・分納情報取込・受注残再構築。 | COMM_ftp（推定。要確認） | |
| 12 | FTP Flow | FVCH001 | CH001連携データ取込。 | | 旧`D:\sqlldr_2018`ディレクトリー使用（現行`%LYR_SQLBAT_DIR%`と不一致）。タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 13 | FTP Flow | FVCH003 | CH003連携データ取込。 | | 理由は同上（FVCH001参照） |
| 14 | FTP Flow | FVGAD68 | GAD68連携データ取込。 | | 理由は同上（FVCH001参照） |
| 15 | FTP Flow | FVGAD69 | GAD69連携データ取込。 | | 理由は同上（FVCH001参照） |
| 16 | FTP Flow | FVKRD21 | 送付先マスタ取込・全件更新。 | COMM_ftp（推定。要確認） | |
| 17 | FTP Flow | FVKRD22 | 送付先マスタ取込・差分反映。 | COMM_ftp（推定。要確認） | |
| 18 | FTP Flow | FVKRD23 | 取引先マスタ取込。 | | 理由は同上（FVCH001参照） |
| 19 | FTP Flow | FVKRD27 | KRD27マスターデータ取込。 | | 理由は同上（FVCH001参照） |
| 20 | FTP Flow | FVKRD28 | KRD28マスターデータ取込。 | | 理由は同上（FVCH001参照） |
| 21 | FTP Flow | FVKRD69 | 取引先マスタデータ取込。 | COMM_ftp（推定。要確認） | |
| 22 | Web API Flow | VDRAA001 | 受注メモ・受注残API連携取込。 | | タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 23 | Web API Flow | VDRAD003 | 受注連携API取込（VDRAD003）。タスクは`.\WebApi_Service.wsf VDRAD003`を直接起動（ソース確認済）。 | WebApi_Service | |
| 24 | Web API Flow | VDRAD004 | 受注連携API取込（VDRAD004）。タスクは`.\WebApi_Service.wsf VDRAD004`を直接起動（ソース確認済）。 | WebApi_Service | |
| 25 | Web API Flow | WebApi_VDRAD003_004 | 受注連携API一括取込（VDRAD003/004）。 | | タスクは`WebApi_Service.wsf`を個別呼出しており、本ファイル（一括版）が直接起動される形跡なし |
| 26 | Web API Flow | VDRAM001 | KCAF・出荷指示API連携取込。実体は`.\WebApi_Service.wsf VDRAM001`（ソース確認済）。 | WebApi_Service | |
| 27 | Web API Flow | VDRAM004 | 出荷連携API取込（VDRAM004）。実体は`.\WebApi_Service.wsf VDRAM004`（ソース確認済）。 | WebApi_Service | |
| 28 | Web API Flow | WebApi_VDRAM001_GD005_GD007 | KCAF・出荷指示API一括取込。 | | 理由は同上（WebApi_VDRAD003_004参照） |
| 29 | Web API Flow | VDRBD002 | API連携取込（VDRBD002）。 | | タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 30 | Web API Flow | VDRGD005 | 出荷指示・KCAF更新API連携取込。実体は`.\WebApi_Service.wsf VDRGD005`（ソース確認済）。 | WebApi_Service | |
| 31 | Web API Flow | VDRGD007 | 出荷指示・KCAF更新API連携取込（007）。実体は`.\WebApi_Service.wsf VDRGD007`（ソース確認済）。 | WebApi_Service | |
| 32 | Curl+VBS Flow | kgss_uriage | 売上実績API連携。curlによる直接呼出（5エンジンのいずれにも該当しない）。 | | |
| 33 | Curl+VBS Flow | kgss_seisan | 生産実績API連携。curlによる直接呼出（同上）。 | | |
| 34 | Curl+VBS Flow | kgss_juchuzan | 受注残API連携。curlによる直接呼出（同上）。 | | |
| 35 | Curl+VBS Flow | kaigaiinv_shukkashiji | 海外INV出荷指示API連携。 | postWebAPI（推定。要確認） | |
| 36 | 共通バッチエンジン | COMM_ftp | 共通バッチエンジン（FTP取得・標準系）。`COMM_FTP_<ID>.bat`等のFTP系バッチから`COMM_ftp.bat <対象ID>`の形で呼ばれる共通部品（ソースで確認済）。呼出元一覧は[COMM_ftp](<../08-システム機能設計書/8-2_バッチ処理定義書/[Sample]COMM_ftp/COMM_ftp_08_外部リクエスト仕様.md>)「5. 呼出元一覧」参照。 | | |
| 37 | 共通バッチエンジン | COMM_ftp10 | 共通バッチエンジン（FTP取得・10系）。`COMM_ftp.bat`と同系統の共通部品（10系サーバー向け）。 | | |
| 38 | 共通バッチエンジン | COMM_ftpSO | 共通バッチエンジン（FTP取得・SO系）。`COMM_ftp.bat`と同系統の共通部品（SO系サーバー向け）。 | | |
| 39 | 共通バッチエンジン | WebApi_Service | 共通バッチエンジン（WebAPI取得・標準系）。`WebApi_VDRAD003`等のWeb API系バッチから`WebApi_Service.wsf <対象ID>`の形で呼ばれる共通部品（タスクが直接`.wsf`を起動するケースも含む。ソースで確認済）。 | | |
| 40 | 共通バッチエンジン | postWebAPI | 共通バッチエンジン（先行POST＋WebAPI取得系）。`kaigaiinv_shukkashiji.bat`等、先行POSTを要するバッチから呼ばれる共通部品。 | | |
| 41 | Other Batch | LYR19_UPDATE_DATA_RENKEI_CHECKER | 連携データ更新チェック（LYR19）。 | | |
| 42 | Other Batch | LYR03_EXP_TBL_RENKEI | 連携テーブル出力（LYR03）。 | | タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 43 | Other Batch | kgss_seisan_up_cb52 | 生産実績（CB52）更新（LYR07/19）。 | | **KCCS確認済み（2026-09-03、課題整理#5）**：使用していると思われる。ソース内に`rem`でコメントアウトされた行（旧LYR07向け）が残存しており、その扱いは未回答のため客先確認待ち（0-8節） |
| 44 | Other Batch | goVDRAD002 | 受注速報・確定反映取込（VDRAD002）。 | | **KCCS確認済み（2026-09-03、課題整理#5）**：現在は使用しておらず、テーブルVDRAD002も現環境に存在しない。ただしソースは存在するためspecは作成する |
| 45 | Other Batch | SP_UPDATE_NOUNYU_JISSEKI | 納入実績更新SP実行。タスク側コメント:「R判定になった分納の実着日を転記」。 | | |
| 46 | Other Batch | SP_JCHZN_TBL_KOKUNAI | 国内受注残更新SP実行。 | | |
| 47 | Other Batch | SHUKKA | SQL_UP_2018更新実行（SHUKKA）。`SeisanUpdate_new.py`の`config.ini`（`LOAD_BAT`）から`subprocess`で呼ばれる（ソース確認済）。実体は`cscript SHUKKA.VBS`を呼ぶ薄いラッパー`SHUKKA.bat`。バッチ処理定義書は未作成（[使い方]0-2節参照）。 | | |
| 48 | Other Batch | ftpget | FTPデータ取得実行。 | | タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 49 | Other Batch | DB_BKUP | 業務テーブルバックアップ。 | | |
| 50 | Other Batch | WebAPI_Monitor | WebAPI稼働監視。 | | タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 51 | Other Batch | SeisanUpdate_sql | 精算更新SQL実行。`SeisanUpdate_new.py`の`config.ini`（`UPDATE_BAT`）から`subprocess`で呼ばれる（ソース確認済）。実体は`sqlplus`で`SeisanUpdate.sql`（`LYR03_EXP_TBL`をJCHZN_TBLから補完する1件のUPDATE文）を実行する薄いラッパー`SeisanUpdate_sql.bat`。バッチ処理定義書は未作成（[使い方]0-2節参照）。 | | |
| 52 | Other Batch | SeisanUpdate_new | 精算更新（新フロー）実行 — 起動ラッパー。本体3行のみ：`cd /d D:\scsales\LYR07` → `venv\Scripts\activate.bat` → `SeisanUpdate_new.py`を起動する薄いラッパー（ソース確認済）。実処理はNo.57（`SeisanUpdate_new.py`）参照。 | | バッチ処理定義書は未作成（サンプルは薄いwrapper例として[COMM_FTP_FVCC011](<../08-システム機能設計書/8-2_バッチ処理定義書/[Sample]COMM_FTP_FVCC011/index.md>)を参照） |
| 53 | Other Batch | SeisanUpdate | 精算更新（標準フロー）実行。ソース上は`SeisanUpdate.py`を起動する、`SeisanUpdate_new.bat`と同型のラッパー。 | | タスクスケジューラに対応するタスクなし。使用実態は不明だが、ソースが存在するためspecは作成する |
| 54 | Other Batch | QuantityEstimation | 数量見積計算実行。 | | 理由は同上（SeisanUpdate参照） |
| 55 | Other Batch | kcaf01_sql | KCAF01更新SQL実行。 | | 理由は同上（SeisanUpdate参照） |
| 56 | Other Batch | KCAF01 | KCAF01業務処理実行。 | | 理由は同上（SeisanUpdate参照） |
| 57 | Other Batch | SeisanUpdate_new.py | 精算更新新フロー（Python本体）。`SeisanUpdate_new.bat`（No.52）から起動される処理本体（ソース確認済：`cd /d D:\scsales\LYR07` → `venv\Scripts\activate.bat` → `SeisanUpdate_new.py`）。 | | バッチ処理定義書は未作成（サンプルは実処理の記入例として[goFVCC011](<../08-システム機能設計書/8-2_バッチ処理定義書/[Sample]goFVCC011/index.md>)を参照） |

///

/// tab | 文書情報・改定履歴

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 6 | 6.3 | バッチ一覧 | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |

///
