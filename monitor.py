import os
import time
import json
import base64
import hashlib
import datetime as dt
from pathlib import Path

import openai
from openai import OpenAI
from dotenv import load_dotenv
import mss
import mss.tools
import pyautogui
from PIL import Image


CAPTURE_INTERVAL_S = 60
SESSION_DURATION_MIN = 480
TMP_DIR = Path("captures")
TMP_DIR.mkdir(exist_ok=True)
EMBED_MODEL = "text-embedding-3-small"
VISION_MODEL = "gpt-4.1-nano"


def load_api_key():
    load_dotenv(".env.local", override=True)
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = key
    return OpenAI()


def grab_active_window():
    bbox = pyautogui.getActiveWindow().box
    with mss.mss() as sct:
        img = sct.grab({"left": bbox[0], "top": bbox[1], "width": bbox[2], "height": bbox[3]})
    return img


def save_active_window_to_png(img, path):
    mss.tools.to_png(img.rgb, img.size, output=str(path))


def summarize_screenshot(client: OpenAI, png_bytes: bytes) -> str:
    b64 = base64.b64encode(png_bytes).decode()
    resp = client.responses.create(
        model=VISION_MODEL,
        input=[{
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "You are an analyst. In \u2264 20 words, describe the user's primary work task in this screenshot. Then list application names and any visible filenames. Use the format Analysis: --- \n Application names: --- \n Visible filenames: --- \n Open tabs: ---"
                },
                {"type": "input_image", "image_url": f"data:image/png;base64,{b64}"}
            ],
        }],
    )
    return resp.output_text


def format_output(ts: str, meta_raw: str) -> str:
    ans = f"\n\U0001F5BC\uFE0F  {ts}\n"
    ans += meta_raw if meta_raw else "None"
    return ans


def run_capture_session():
    client = load_api_key()
    records = []
    start = time.time()
    print(f"Running capture loop for {SESSION_DURATION_MIN} minutes …")
    while (time.time() - start) < SESSION_DURATION_MIN * 60:
        img = grab_active_window()
        png = mss.tools.to_png(img.rgb, img.size)
        phash = hashlib.sha1(png).hexdigest()
        if records and phash == records[-1]["phash"]:
            time.sleep(CAPTURE_INTERVAL_S)
            continue
        meta_raw = summarize_screenshot(client, png)
        stamp = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        meta = format_output(stamp, meta_raw)
        records.append({"timestamp": stamp, "phash": phash, "meta": meta})
        print(meta)
        save_active_window_to_png(img, TMP_DIR / f"{stamp}.png")
        time.sleep(CAPTURE_INTERVAL_S)
    print("Loop finished")
    return records


if __name__ == "__main__":
    run_capture_session()
