from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"

# تأكد أن مجلد التنزيل موجود
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')

    if not video_url:
        return render_template('index.html', error='لم يتم إدخال رابط الفيديو')

    try:
        video_id = str(uuid.uuid4())
        filepath = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'best[ext=mp4]/best',
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return render_template('index.html', download_url=f'/get_video/{video_id}')

    except Exception as e:
        print("خطأ أثناء تحميل الفيديو:", e)
        return render_template('index.html', error="فشل في تحميل الفيديو. تأكد من صحة الرابط.")

@app.route('/get_video/<video_id>')
def get_video(video_id):
    filepath = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "الملف غير موجود", 404
