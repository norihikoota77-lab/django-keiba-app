import os
import random
import pandas as pd
import openpyxl
import tempfile
import traceback
import urllib.parse
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, Http404
from .forms import UploadForm
from .scoring_engine import ScoringEngine


def index(request):
    """ファイル選択および処理のビュー"""
    form = UploadForm()
    
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            correct_file = request.FILES["correct_file"]
            user_file = request.FILES["user_file"]

            # アップロードされたファイルを一時ファイルとして保持
            c_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
            u_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
            
            try:
                for chunk in correct_file.chunks():
                    c_temp.write(chunk)
                for chunk in user_file.chunks():
                    u_temp.write(chunk)
                
                c_temp.close()
                u_temp.close()
                
                c_path = c_temp.name
                u_path = u_temp.name

                # 正解ファイルのB13セルからタイトルを取得
                correct_title = "タイトル不明"
                try:
                    wb_c = openpyxl.load_workbook(c_path, data_only=True)
                    ws_c = wb_c.active
                    if ws_c['B13'].value:
                        correct_title = str(ws_c['B13'].value)
                except Exception as e:
                    pass

                # ユーザーファイルのB13セルから名前を取得
                user_name = "名無し"
                try:
                    wb_u = openpyxl.load_workbook(u_path, data_only=True)
                    ws_u = wb_u.active
                    if ws_u['B13'].value:
                        raw_name = str(ws_u['B13'].value)
                        user_name = "".join(c for c in raw_name if c not in r'\/:*?"<>|')
                except Exception as e:
                    pass

                # パス文字列へ変換して結合し、保存先フォルダを作成
                output_dir = os.path.join(str(settings.BASE_DIR), "reports")
                os.makedirs(output_dir, exist_ok=True)
                
                output_file = os.path.join(
                    output_dir, f"{user_name}_{os.path.splitext(user_file.name)[0]}_レース結果報告.xlsx"
                )

                engine = ScoringEngine()
                engine.grade(c_path, u_path)
                engine.export_excel(output_file)

                msg, color = engine.get_result_message()

                # スコアに応じた動画フォルダの振り分け
                if engine.percentage >= 80:
                    folder_name = "excellent"
                elif engine.percentage >= 50:
                    folder_name = "good"
                else:
                    folder_name = "try_again"

                static_videos_dir = os.path.join(str(settings.BASE_DIR), 'keiba_app', 'static', 'videos')
                folder_path = os.path.join(static_videos_dir, folder_name)
                video_file = f"videos/{folder_name}/default.mp4"

                if os.path.exists(folder_path):
                    mp4_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp4')]
                    if mp4_files:
                        selected_file = random.choice(mp4_files)
                        video_file = f"videos/{folder_name}/{selected_file}"

                file_name = os.path.basename(output_file)

                report_html = ""
                if os.path.exists(output_file):
                    try:
                        df = pd.read_excel(output_file)
                        df.columns = [str(col).split('.')[0] for col in df.columns]
                        report_html = df.to_html(
                            classes='dataframe',
                            border=0,
                            index=False,
                            justify="center",
                            escape=False
                        )
                        report_html = report_html.replace('✖', '<span class="text-blue-600 font-bold">✖</span>')
                    except Exception as e:
                        report_html = f"<p class='text-red-500'>プレビュー読み込みエラー: {e}</p>"

                context = {
                    "score": engine.score,
                    "valid_count": engine.valid_count,
                    "percentage": engine.percentage,
                    "rank": engine.get_rank(),
                    "msg": msg,
                    "color": color,
                    "report_file_name": file_name,
                    "report_html": report_html,
                    "video_file": video_file,
                    "user_name": user_name,
                    "correct_title": correct_title,  # 追加: タイトル情報
                }

                return render(request, "result.html", context)

            except Exception as e:
                print("--- [採点処理でエラーが発生しました] ---")
                traceback.print_exc()
                return render(request, "index.html", {"form": form, "error": f"処理中にエラーが発生しました: {str(e)}"})

            finally:
                # 一時ファイルの確実に削除
                if os.path.exists(c_temp.name):
                    os.remove(c_temp.name)
                if os.path.exists(u_temp.name):
                    os.remove(u_temp.name)
        
        else:
            return render(request, "index.html", {"form": form, "error": "入力されたファイルが無効です。"})

    return render(request, "index.html", {"form": form})


def download_report(request, file_name):
    """ファイルをダウンロードさせる専用ビュー"""
    decoded_file_name = urllib.parse.unquote(file_name)
    file_path = os.path.join(str(settings.BASE_DIR), 'reports', decoded_file_name)
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{urllib.parse.quote(decoded_file_name)}"
        return response
    else:
        raise Http404(f"ファイルが見つかりません: {file_path}")