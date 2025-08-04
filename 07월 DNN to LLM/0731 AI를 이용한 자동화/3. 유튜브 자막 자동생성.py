from pytubefix import YouTube
from openai import OpenAI
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=O-ZfXbfAMKU"
yt = YouTube(url, on_progress_callback=on_progress)
yt.title
ys = yt.streams.get_highest_resolution()
ys.download()
ys_audio = yt.streams.get_audio_only()
ys_audio.download()
file_path = '/home/play/workspace/Codex CLI with codex-mini.m4a'

client = OpenAI()
with open(file_path, "rb") as audio:
    script = client.audio.transcriptions.create(
        model='whisper-1',
        response_format='srt',
        file=audio
    )

with open(file_path.replace("m4a", 'srt'), 'w', encoding='utf-8') as f:
    f.write(script)
