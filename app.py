from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
        <form method='post' action='/download'>
            <input name='url' type='text' placeholder='Enter YouTube URL'>
            <button type='submit'>Download MP3</button>
        </form>
    """

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
