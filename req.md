keiba_project/              # プロジェクトルート
├── manage.py
├── keiba_app/              # アプリケーション
│   ├── __init__.py
│   ├── scoring_engine.py  # ★ ScoringEngine をここに移動
│   ├── forms.py           # アップロードフォームの定義
│   ├── views.py           # リクエスト処理と採点ロジックの呼び出し
│   └── urls.py            # URLルーティング
├── media/                 # ★ アップロードファイルやレポートの保存先
├── templates/             # HTMLファイル
│   ├── index.html         # ファイル選択画面
│   └── result.html        # レース結果表示画面
└── static/                # CSSや画像、動画ファイルなど
