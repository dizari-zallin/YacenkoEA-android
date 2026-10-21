# -*- coding: utf-8 -*-
"""Capture the open Android Studio window with PrintWindow. Does not activate it."""
import ctypes
import json
import subprocess
import time
from ctypes import wintypes
from pathlib import Path

from PIL import Image

STUDIO = r"C:\Program Files\Android\Android Studio\bin\studio64.exe"
ROOT = Path(r"C:\Users\Shmurdyakich\Desktop\androidALL")
PROJECTS = ROOT / "projects"
SHOTS = ROOT / "screenshots"

FILES = {
    1: "app/src/main/java/com/yacenkoea/pr1/MainActivity.java",
    2: "app/src/main/java/com/yacenkoea/pr2/MainActivity.java",
    3: "app/src/main/java/com/yacenkoea/pr3/MainActivity.java",
    4: "app/src/main/res/values/my_colors.xml",
    5: "app/src/main/java/com/yacenkoea/pr5/MainActivity.java",
    6: "app/src/main/java/com/yacenkoea/pr6/MainActivity.java",
    7: "app/src/main/java/com/yacenkoea/pr7/MainActivity.java",
    8: "app/src/main/java/com/yacenkoea/pr8/MainActivity.java",
    9: "app/src/main/java/com/yacenkoea/pr9/MainActivity.java",
    10: "app/src/main/java/com/yacenkoea/pr10/MainActivity.java",
    11: "app/src/main/res/drawable/animation.xml",
    12: "app/src/main/res/anim/rotate_center.xml",
    13: "app/src/main/res/drawable/sun.xml",
    14: "app/src/main/java/com/yacenkoea/pr14/MainActivity.java",
}

CAPTIONS = {
    1: "Проект YacenkoEA_PR1 в Android Studio, класс MainActivity",
    2: "Проект YacenkoEA_PR2 в Android Studio, обработчик кнопки",
    3: "Проект YacenkoEA_PR3 в Android Studio, счётчик нажатий",
    4: "Файл цветовых ресурсов my_colors.xml проекта YacenkoEA_PR4",
    5: "Проект YacenkoEA_PR5 в Android Studio, переход между окнами",
    6: "Проект YacenkoEA_PR6 в Android Studio, передача данных студента",
    7: "Проект YacenkoEA_PR7 в Android Studio, возврат результата",
    8: "Проект YacenkoEA_PR8 в Android Studio, выбор изображения",
    9: "Проект YacenkoEA_PR9 в Android Studio, воспроизведение звука",
    10: "Проект YacenkoEA_PR10 в Android Studio, воспроизведение видео",
    11: "Список кадров animation.xml проекта YacenkoEA_PR11",
    12: "Анимация rotate_center.xml проекта YacenkoEA_PR12",
    13: "Фигура sun.xml проекта YacenkoEA_PR13",
    14: "Проект YacenkoEA_PR14 в Android Studio, тест из пяти вопросов",
}

u = ctypes.windll.user32
gdi = ctypes.windll.gdi32
PW_RENDERFULLCONTENT = 2


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", ctypes.c_uint32),
        ("biWidth", ctypes.c_int32),
        ("biHeight", ctypes.c_int32),
        ("biPlanes", ctypes.c_uint16),
        ("biBitCount", ctypes.c_uint16),
        ("biCompression", ctypes.c_uint32),
        ("biSizeImage", ctypes.c_uint32),
        ("biXPelsPerMeter", ctypes.c_int32),
        ("biYPelsPerMeter", ctypes.c_int32),
        ("biClrUsed", ctypes.c_uint32),
        ("biClrImportant", ctypes.c_uint32),
    ]


def windows():
    found = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def cb(hwnd, _):
        if u.IsWindowVisible(hwnd):
            n = u.GetWindowTextLengthW(hwnd)
            if n:
                buf = ctypes.create_unicode_buffer(n + 1)
                u.GetWindowTextW(hwnd, buf, n + 1)
                title = buf.value
                low = title.casefold()
                if any(part in low for part in ("yacenkoea", "android studio", "mainactivity.java", ".xml")):
                    found.append((hwnd, title))
        return True

    u.EnumWindows(cb, 0)
    return found


def grab(hwnd, dest):
    rect = wintypes.RECT()
    u.GetWindowRect(hwnd, ctypes.byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top
    if w < 400 or h < 300:
        return False
    hdc = u.GetWindowDC(hwnd)
    mem = gdi.CreateCompatibleDC(hdc)
    bmp = gdi.CreateCompatibleBitmap(hdc, w, h)
    gdi.SelectObject(mem, bmp)
    ok = u.PrintWindow(hwnd, mem, PW_RENDERFULLCONTENT)
    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    buf = ctypes.create_string_buffer(w * h * 4)
    rows = gdi.GetDIBits(mem, bmp, 0, h, buf, ctypes.byref(bmi), 0)
    gdi.DeleteObject(bmp)
    gdi.DeleteDC(mem)
    u.ReleaseDC(hwnd, hdc)
    if not ok or not rows:
        return False
    Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB").save(dest)
    return True


def prepend(n, path, caption):
    folder = SHOTS / f"pr{n}"
    meta = folder / "captions.json"
    data = json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else []
    data = [item for item in data if "studio" not in Path(item["file"]).name]
    data.insert(0, {"file": str(path), "caption": caption, "wide": True})
    meta.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def open_file(path):
    subprocess.Popen([STUDIO, str(path)])


def matches(title, n, token):
    low = title.casefold()
    if token != "MainActivity.java":
        return token.casefold() in low
    import re
    return re.search(rf"[\\/]pr{n}(?!\d)", low) is not None


def wait_title(n, token, seconds=40):
    deadline = time.time() + seconds
    last = ""
    while time.time() < deadline:
        items = windows()
        if items:
            last = items[0][1]
            hit = next((item for item in items if matches(item[1], n, token)), None)
            if hit:
                time.sleep(1.2)
                items = windows()
                hit = next((item for item in items if matches(item[1], n, token)), hit)
                return hit
        time.sleep(0.4)
    return None, last


def main():
    for n, rel in FILES.items():
        name = f"YacenkoEA_PR{n}"
        path = PROJECTS / name / rel
        token = Path(rel).name
        print(f"open {name} {token}", flush=True)
        open_file(path)
        hwnd, title = wait_title(n, token, 100 if n == 1 else 40)
        print(f"title {title}", flush=True)
        dest = SHOTS / f"pr{n}" / "studio.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if hwnd and grab(hwnd, dest):
            prepend(n, dest, CAPTIONS[n])
            print(f"saved {dest}", flush=True)
        else:
            print(f"MISS {name}", flush=True)
        time.sleep(1)
    pr1 = SHOTS / "pr1" / "studio.png"
    if pr1.exists():
        intro = SHOTS / "pr0" / "studio.png"
        intro.write_bytes(pr1.read_bytes())
        prepend(0, intro, "Окно Android Studio с открытым учебным проектом")


if __name__ == "__main__":
    main()
