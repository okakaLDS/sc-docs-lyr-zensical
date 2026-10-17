---
title: "業務フロー（サンプル）"
tags:
  - SC作成
  - 業務設計書
owner: "SC様"
doc_no: "3.1"
---

# 業務フロー — サンプル（記入例）

/// tab | 本文


*記入イメージの例であり、実データではない。空テンプレートは 空テンプレート、記法は 使い方 を参照。
本書は稼働中システムで行われている業務をそのまま記述する（現行のみ）。将来の業務変更案・改修案は本書に含めない。*

## 1. 業務一覧

| 業務No. | 業務名 | 範囲（起点〜終点） | 主な関係者 |
| ------- | ------ | ------------------ | ---------- |
| 1 | 納期回答 | 客先の注文書受領から、客先への納期回答・合意まで | お客様／販社、営業、CS営業、製造部門 |
| 2 | 出荷確認 | 出荷予定日の前日確認から、出荷可否の確定まで | CS営業、製造部門、物流 |

## 2. 業務フロー

### 2-1. ＜業務1：納期回答＞

```mermaid
sequenceDiagram
  autonumber

  box rgb(232,240,254) 社外
    actor CUS as （国内）お客様<br/>（海外）販社
  end
  box rgb(255,244,229) 営業側
    actor SLS as 営業
    actor CS as CS営業
  end
  box rgb(232,245,233) 製造側
    actor MFG as 製造部門
  end
  box rgb(238,238,238) システム
    participant SYS as 本システム
    participant DB as 台帳／DB
  end

  Note over CUS,SLS: ① 注文入手
  CUS->>SLS: 注文書を発行
  activate SLS
  SLS->>SLS: 記載内容を確認
  alt 不備あり
    SLS--)CUS: 差戻し連絡
    Note right of SLS: 修正後に再提出
  else 不備なし
    SLS->>CS: 注文書を引き渡し
  end
  deactivate SLS

  Note over CS,DB: ② 注文情報の登録
  activate CS
  CS->>SYS: 注文情報を入力
  SYS->>DB: 注文データを登録
  DB-->>SYS: 採番結果を返却
  SYS-->>CS: 登録完了
  deactivate CS

  Note over CS,MFG: ③ 製造への依頼〜回答
  CS->>MFG: 投入依頼
  activate MFG
  MFG->>MFG: 生産可否を判定
  MFG->>SYS: 回答納期を登録
  MFG--)CS: 回答納期を通知
  deactivate MFG

  Note over CUS,CS: ④ 納期合意
  CS-->>CUS: 客先へ納期回答
  CUS->>CUS: 納期を確認し合意
```

### 2-2. ＜業務2：出荷確認＞

```mermaid
sequenceDiagram
  autonumber

  box rgb(255,244,229) 営業側
    actor CS as CS営業
  end
  box rgb(232,245,233) 製造側
    actor MFG as 製造部門
    actor LOG as 物流
  end
  box rgb(238,238,238) システム
    participant SYS as 本システム
  end

  Note over CS,SYS: ① 出荷予定の確認
  CS->>SYS: 翌日出荷予定を照会
  SYS-->>CS: 出荷予定一覧を表示

  Note over CS,MFG: ② 出荷可否の確認
  CS->>MFG: 完成状況を確認
  activate MFG
  alt 完成済み
    MFG-->>CS: 出荷可
  else 未完成
    MFG-->>CS: 出荷不可（理由と見込み日）
    CS->>SYS: 納期を再調整（業務1 ④へ）
  end
  deactivate MFG

  Note over CS,LOG: ③ 出荷指示
  CS->>SYS: 出荷確定を登録
  SYS--)LOG: 出荷指示を通知
```

///

/// tab | 文書情報・改定履歴

## 文書情報

| 大分類 | 小分類 | ドキュメント名 | システムID | システム名 |
| ------ | ------ | -------------- | ---------- | ---------- |
| 3 | 3.1 | 業務フロー | AZR | 納期管理システム |

## 改定履歴

| Version | 計画書No. | 改訂日     | 改訂内容 | 担当者 | 課題No./備考 |
| ------- | --------- | ---------- | -------- | ------ | ------------ |
| 1.0.0 | K2603-A002 | 2026-09-29 | 新規作成 | KCCS(岡) | - |

///
