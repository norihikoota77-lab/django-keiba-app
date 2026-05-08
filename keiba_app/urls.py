from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ダウンロード用のURLパスを追加
    path('reports/<str:file_name>/', views.download_report, name='download_report'),
]