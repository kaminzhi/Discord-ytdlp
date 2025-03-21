import subprocess


def get_formats(url):
    """獲取影片的所有可用格式（解析度選項）"""
    try:
        process = subprocess.run(,
            shell=True,
            capture_output=True,
            text=True,
        )

        output = process.stdout.strip()
        error = process.stderr.strip()

        if process.returncode == 0:
            formats = output.splitlines()
            available_formats = []

            for fmt in formats:
                parts = fmt.split(" - ")
                resolution = parts[0]
                format_id = parts[1]
                fps = parts[2] if len(parts) > 2 else "N/A"
                available_formats.append(
                    {"resolution": resolution, "format_id": format_id, "fps": fps}
                )

            return True, available_formats  # 回傳所有可用格式
        else:
            return False, error

    except Exception as e:
        return False, str(e)


def get_video(url, format_id):
    try:
        process = subprocess.run(
            f"python3 scripts/download_script.py {url} {format_id}",
            shell=True,
            capture_output=True,
            text=True,
        )

        output = process.stdout.strip()
        error = process.stderr.strip()

        if process.returncode == 0:
            return True, output
        else:
            return False, error

    except Exception as e:
        return False, str(e)
