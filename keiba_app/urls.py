from django.urls import path
from . import views
# --- 以下の2行を追加 ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    # ダウンロード用のURLパス
    path('reports/<str:file_name>/', views.download_report, name='download_report'),
]

# --- メディアファイル（動画・エクセル）をブラウザで表示するための設定 ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # ついでに静的ファイルも開発環境で確認できるようにする場合
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)