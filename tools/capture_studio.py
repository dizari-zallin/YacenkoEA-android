# -*- coding: utf-8 -*-
"""Opens each lab in Android Studio and saves a window screenshot."""
import ctypes
import json
import subprocess
import time
from ctypes import wintypes
from pathlib import Path

from PIL import ImageGrab

STUDIO = Path(r"C:\Program Files\Android\Android Studio\bin\studio64.exe")
ROOT = Path(r"C:\Users\Shmurdyakich\Desktop\androidALL")
PROJECTS = ROOT / "projects"
OUT = ROOT / "screenshots"
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

FILES = {
    0: PROJECTS / "Shmurdyakich_PR1" / "app/src/main/java/com/shmurdyakich/pr1/MainActivity.java",
    1: PROJECTS / "Shmurdyakich_PR1" / "app/src/main/java/com/shmurdyakich/pr1/MainActivity.java",
    2: PROJECTS / "Shmurdyakich_PR2" / "app/src/main/java/com/shmurdyakich/pr2/MainActivity.java",
    3: PROJECTS / "Shmurdyakich_PR3" / "app/src/main/java/com/shmurdyakich/pr3/MainActivity.java",
    4: PROJECTS / "Shmurdyakich_PR4" / "app/src/main/res/values/my_colors.xml",
    5: PROJECTS / "Shmurdyakich_PR5" / "app/src/main/java/com/shmurdyakich/pr5/MainActivity.java",
    6: PROJECTS / "Shmurdyakich_PR6" / "app/src/main/java/com/shmurdyakich/pr6/MainActivity.java",
    7: PROJECTS / "Shmurdyakich_PR7" / "app/src/main/java/com/shmurdyakich/pr7/MainActivity.java",
    8: PROJECTS / "Shmurdyakich_PR8" / "app/src/main/java/com/shmurdyakich/pr8/MainActivity.java",
    9: PROJECTS / "Shmurdyakich_PR9" / "app/src/main/java/com/shmurdyakich/pr9/MainActivity.java",
    10: PROJECTS / "Shmurdyakich_PR10" / "app/src/main/java/com/shmurdyakich/pr10/MainActivity.java",
    11: PROJECTS / "Shmurdyakich_PR11" / "app/src/main/res/drawable/animation.xml",
    12: PROJECTS / "Shmurdyakich_PR12" / "app/src/main/res/anim/rotate_center.xml",
    13: PROJECTS / "Shmurdyakich_PR13" / "app/src/main/res/drawable/sun.xml",
    14: PROJECTS / "Shmurdyakich_PR14" / "app/src/main/java/com/shmurdyakich/pr14/MainActivity.java",
}

CAPTIONS = {
    0: "Главное окно Android Studio с открытым проектом",
    1: "Android Studio: класс MainActivity и структура проекта",
    2: "Android Studio: обработчик нажатия кнопки в MainActivity",
    3: "Android Studio: счётчик нажатий в обработчике onClick",
    4: "Android Studio: файл цветовых ресурсов my_colors.xml",
    5: "Android Studio: переход между активностями в MainActivity",
    6: "Android Studio: передача объекта Student через Intent",
    7: "Android Studio: регистрация Activity Result API",
    8: "Android Studio: загрузка изображения и масштаб ImageView",
    9: "Android Studio: класс аудиоплеера на MediaPlayer",
    10: "Android Studio: воспроизведение видео через VideoView",
    11: "Android Studio: описание покадровой анимации animation.xml",
    12: "Android Studio: анимация вращения rotate_center.xml",
    13: "Android Studio: фигура солнца sun.xml",
    14: "Android Studio: логика мини-викторины",
}


def enum_windows():
    found = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        found.append((hwnd, buf.value))
        return True

    user32.EnumWindows(cb, 0)
    return found


def studio_window(expect):
    for hwnd, title in enum_windows():
        if expect.lower() in title.lower():
            return hwnd, title
    return None, ""


def grab(hwnd, dest: Path):
    user32.ShowWindow(hwnd, 3)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.8)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    img = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    print("saved", dest, img.size)


def append_caption(n, dest, caption):
    meta = OUT / f"pr{n}" / "captions.json"
    items = []
    if meta.exists():
        items = json.loads(meta.read_text(encoding="utf-8"))
    items.insert(0, {"file": str(dest), "caption": caption, "wide": True})
    meta.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def open_file(path: Path):
    subprocess.Popen([str(STUDIO), str(path)])


def dismiss_dialogs():
    for hwnd, title in enum_windows():
        low = title.lower()
        if any(word in low for word in ("trust", "recommended", "update", "open project")):
            user32.ShowWindow(hwnd, 9)
            user32.SetForegroundWindow(hwnd)
            time.sleep(0.4)
            user32.keybd_event(0x0D, 0, 0, 0)
            user32.keybd_event(0x0D, 0, 2, 0)
            print("dialog", title)
            time.sleep(1.2)


def wait_title(token, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        dismiss_dialogs()
        hwnd, title = studio_window(token)
        if hwnd:
            return hwnd, title
        time.sleep(2)
    return None, ""


def main():
    options = Path.home() / "AppData/Roaming/Google/AndroidStudio2026.1.4/options"
    options.mkdir(parents=True, exist_ok=True)
    entries = []
    for n in range(1, 15):
        path = str(PROJECTS / f"Shmurdyakich_PR{n}")
        entries.append(f'        <entry key="{path}" value="true" />')
    trusted = options / "trusted-paths.xml"
    trusted.write_text(
        """<application>
  <component name="Trusted.Paths">
    <option name="TRUSTED_PROJECT_PATHS">
      <map>
""" + "\n".join(entries) + """
      </map>
    </option>
  </component>
</application>
""",
        encoding="utf-8",
    )

    first = True
    for n in range(1, 15):
        project = PROJECTS / f"Shmurdyakich_PR{n}"
        code = FILES[n]
        token = f"PR{n}"
        print("open project", project.name, flush=True)
        open_file(project)
        hwnd, title = wait_title(token, 200 if first else 100)
        if not hwnd:
            print("project window missing, opening file", flush=True)
            open_file(code)
            hwnd, title = wait_title(code.name, 40)
        else:
            time.sleep(4)
            open_file(code)
            hwnd2, title2 = wait_title(code.name, 30)
            if hwnd2:
                hwnd, title = hwnd2, title2
        first = False
        if not hwnd:
            print("NO WINDOW", project.name, flush=True)
            continue
        print("window", title, flush=True)
        time.sleep(6)
        dest = OUT / f"pr{n}" / "studio.png"
        grab(hwnd, dest)
        append_caption(n, dest, CAPTIONS[n])
        if n == 1:
            intro = OUT / "pr0" / "studio.png"
            grab(hwnd, intro)
            append_caption(0, intro, CAPTIONS[0])


if __name__ == "__main__":
    main()
