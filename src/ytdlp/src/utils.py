import json
import yt_dlp


async def get_thumbnail(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        if not info_dict:
            return None

        thumbnail_url = info_dict.get("thumbnail")

        if not thumbnail_url and "thumbnails" in info_dict:
            thumbnails = info_dict["thumbnails"]
            if thumbnails:
                thumbnail_url = max(thumbnails, key=lambda x: x.get("height", 1))["url"]

        return thumbnail_url


async def get_formats(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if not info_dict:
            return "Error 01"
        formats = info_dict.get("formats", [])
        video_formats = []
        seen = set()
        index_map = {}

        for f in formats:
            if (
                "vcodec" in f
                and not f.get("format", "").startswith("sb")
                and f.get("resolution") not in ("audio only", "None")
            ):
                resolution = f.get("resolution", "N/A")
                format_id = f.get("format_id", "N/A")
                fps = float(f.get("fps", 0))

                if (resolution, fps) not in seen:
                    index_map[format_id] = len(video_formats)
                    video_formats.append(
                        {
                            "resolution": resolution,
                            "format_id": format_id,
                            "fps": fps,
                        }
                    )
                    seen.add((resolution, fps))
        if video_formats:
            return json.dumps(video_formats, indent=4)
        else:
            return "Error 02"


"""
async def get_filesize(m4u8_url):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", m4u8_url]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    info = json.loads(stdout.decode())
    filesize = info.get("format", {}).get("size")
    return int(filesize) if filesize else None
"""
