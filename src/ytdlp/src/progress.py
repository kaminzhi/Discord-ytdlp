import time
import aiohttp
import asyncio


def progress_hook(d, tracker=None):
    if tracker:
        tracker.update(d)
    else:
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "N/A")
            speed = d.get("_speed_str", "N/A")
            eta = d.get("_eta_str", "N/A")
            print(f"\rDownloading...: {percent} Speed: {speed}, eta: {eta}", end="")
        elif d["status"] == "finished":
            print("\nProcessing...")
