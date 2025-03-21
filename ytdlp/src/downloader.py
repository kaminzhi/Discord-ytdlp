import os
import aiohttp
import yt_dlp
import asyncio
from . import progress_hook


async def video_downloader(url, format_id=None):
    download_dir = os.environ.get("DOWNLOAD_DIR", "downloads")
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        "format": f"{format_id} + bestaudio/best"
        if format_id
        else "bestvideo+bestaudio/best",
        "outtmpl": f"{download_dir}/%(title)s.%(ext)s",
        "external-downloader": "aria2c",
        "external-downloader-args": "-x 16 -s 16 -k 1M -j 16 --file-allocation=none --optimize-concurrent-downloads=true --min-split-size=1M",
        "progress_hooks": [lambda d: progress_hook(d)],
        "retries": 10,
        "fragment_retries": 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(ydl.record_download_archive(info))
            return ydl.prepare_filename(info)
    except Exception as e:
        return e


async def audio_downloader(url, audio_format=None, quality=None):
    download_dir = os.environ.get("DOWNLOAD_DIR", "downloads")
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format if audio_format else "mp3",
                "preferredquality": quality if quality else "320",
            }
        ],
        "outtmpl": f"{download_dir}/%(title)s.%(ext)s",
        "external-downloader": "aria2c",
        "external-downloader-args": "-x 16 -s 16 -k 1M -j 16 --file-allocation=none --optimize-concurrent-downloads=true --min-split-size=1M",
        "progress_hooks": [lambda d: progress_hook(d)],
        "retries": 10,
        "fragment_retries": 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        return e
