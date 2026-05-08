# 🐎 競馬スコアラー - Django採点システム

Excelファイルをアップロードするだけで、
自動採点・レポート生成・結果可視化を行う Django Webアプリです。

---

# 📸 アプリ概要

正解マスタExcelとユーザー解答Excelを読み込み、

- 自動採点
- 正答率算出
- ランク判定
- HTMLプレビュー
- Excelレポート出力
- フィードバック動画表示

を行います。

---

# 🚀 使用技術

| 技術         | 内容              |
| ------------ | ----------------- |
| Python       | バックエンド処理  |
| Django       | Webフレームワーク |
| Pandas       | Excelデータ処理   |
| openpyxl     | Excelレポート生成 |
| Tailwind CSS | UIデザイン        |
| HTML/CSS     | フロント実装      |

---

# 📂 ディレクトリ構成

```txt
portfolio_kweb/
│
├── keiba_app/
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── result.css
│   │   └── videos/
│   │
│   ├── scoring_engine.py
│   ├── views.py
│   └── urls.py
│
├── reports/
├── data/
├── manage.py
└── requirements.txt
```
