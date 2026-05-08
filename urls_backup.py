from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('keiba_app.urls')),
]

# プロジェクトルートの reports フォルダを配信する設定
if settings.DEBUG:
    urlpatterns += static('/reports/', document_root=settings.BASE_DIR / 'reports')