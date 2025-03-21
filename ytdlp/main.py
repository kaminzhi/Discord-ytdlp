import asyncio

from src import get_formats, get_thumbnail
from src import video_downloader, audio_downloader


async def main():
    num = int(input("Mode:"))
    url = input("URL:")

    if num == 1:
        print(await get_formats(url))
    elif num == 2:
        print(await get_thumbnail(url))
    elif num == 3:
        format_id = input("Format_id:")
        await video_downloader(url, format_id)
    elif num == 4:
        audio_format = input("Audio_format:")
        quality = input("Quality:")
        await audio_downloader(url, audio_format, quality)


asyncio.run(main())
