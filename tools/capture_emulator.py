# -*- coding: utf-8 -*-
"""Installs debug APKs on the running emulator and saves screenshots."""
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ADB = Path.home() / "AppData/Local/Android/Sdk/platform-tools/adb.exe"
BUILD = Path(r"D:\androidALL-build")
OUT = Path(r"C:\Users\Shmurdyakich\Desktop\androidALL\screenshots")
BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


def run(args, check=True, timeout=60):
    return subprocess.run(
        [str(ADB), *args],
        check=check,
        capture_output=True,
        timeout=timeout,
    )


def sh(cmd, check=False):
    return run(["shell", cmd], check=check)


def shot(folder: Path, name: str, caption: str, wide=False, items=None):
    folder.mkdir(parents=True, exist_ok=True)
    remote = "/sdcard/labshot.png"
    sh(f"screencap -p {remote}")
    dest = folder / name
    run(["pull", remote, str(dest)])
    items.append({"file": str(dest), "caption": caption, "wide": wide})
    print("shot", dest.name, dest.stat().st_size)


def dump():
    sh("uiautomator dump /sdcard/uidump.xml")
    raw = run(["exec-out", "cat", "/sdcard/uidump.xml"], check=False).stdout
    text = raw.decode("utf-8", errors="ignore")
    start = text.find("<hierarchy")
    if start < 0:
        return None
    try:
        return ET.fromstring(text[start:])
    except ET.ParseError:
        return None


def center(node):
    m = BOUNDS.search(node.attrib.get("bounds", ""))
    if not m:
        return None
    x1, y1, x2, y2 = map(int, m.groups())
    return (x1 + x2) // 2, (y1 + y2) // 2


def same_text(left, right):
    return left.casefold().strip() == right.casefold().strip()


def tap_text(label, tries=8):
    for _ in range(tries):
        root = dump()
        if root is not None:
            for node in root.iter("node"):
                values = (
                    node.attrib.get("text", ""),
                    node.attrib.get("content-desc", ""),
                )
                if any(same_text(label, v) or (label and label.casefold() in v.casefold() and len(label) > 3) for v in values):
                    point = center(node)
                    if point:
                        sh(f"input tap {point[0]} {point[1]}")
                        time.sleep(0.6)
                        return True
        time.sleep(0.4)
    print("NOT FOUND", label)
    return False


def tap_exact(label, tries=6):
    for _ in range(tries):
        root = dump()
        if root is not None:
            for node in root.iter("node"):
                if same_text(node.attrib.get("text", ""), label):
                    point = center(node)
                    if point:
                        sh(f"input tap {point[0]} {point[1]}")
                        time.sleep(0.5)
                        return True
        time.sleep(0.4)
    print("NOT EXACT", label)
    return False


def input_text(value):
    sh(f"input text {value}")
    time.sleep(0.3)
    sh("input keyevent 111")
    time.sleep(0.3)


def launch(pkg, activity="MainActivity"):
    sh(f"am force-stop {pkg}")
    time.sleep(0.3)
    run(["shell", "am", "start", "-W", "-n", f"{pkg}/.{activity}"], check=False)
    time.sleep(1.4)


def install(n):
    name = f"YacenkoEA_PR{n}"
    apk = BUILD / name / "app" / "outputs" / "apk" / "debug" / "app-debug.apk"
    if not apk.exists():
        raise FileNotFoundError(apk)
    result = run(["install", "-r", "-t", str(apk)], check=False, timeout=120)
    print(name, result.returncode, result.stdout.decode("utf-8", "ignore")[-200:])
    if result.returncode != 0:
        print(result.stderr.decode("utf-8", "ignore")[-500:])
        raise SystemExit(f"install failed {name}")


def save(n, items):
    folder = OUT / f"pr{n}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "captions.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def flow():
    # 1
    install(1)
    items = []
    launch("com.yacenkoea.pr1")
    shot(OUT / "pr1", "emu_hello.png", "Окно эмулятора после запуска проекта: надпись Hello World!", items=items)
    save(1, items)

    # 2
    install(2)
    items = []
    launch("com.yacenkoea.pr2")
    shot(OUT / "pr2", "emu_before.png", "Экран до нажатия кнопки: поле ввода видимо, картинка скрыта", items=items)
    tap_text("Введите текст")
    input_text("Hello")
    tap_exact("Показать")
    time.sleep(0.4)
    shot(OUT / "pr2", "emu_after.png", "Экран после нажатия кнопки: введённый текст и изображение", items=items)
    save(2, items)

    # 3
    install(3)
    items = []
    launch("com.yacenkoea.pr3")
    shot(OUT / "pr3", "emu_zero.png", "Счётчик до нажатий равен нулю", items=items)
    for _ in range(5):
        tap_exact("Нажми меня")
    shot(OUT / "pr3", "emu_five.png", "Счётчик после пяти нажатий на кнопку", items=items)
    save(3, items)

    # 4
    install(4)
    items = []
    launch("com.yacenkoea.pr4")
    shot(OUT / "pr4", "emu_resources.png", "Строка и цвета, взятые из ресурсов strings.xml, headers.xml и my_colors.xml", items=items)
    save(4, items)

    # 5
    install(5)
    items = []
    launch("com.yacenkoea.pr5")
    shot(OUT / "pr5", "emu_first.png", "Первая активность", items=items)
    tap_exact("Открыть второе окно")
    time.sleep(0.8)
    shot(OUT / "pr5", "emu_second.png", "Вторая активность после перехода по кнопке", items=items)
    save(5, items)

    # 6
    install(6)
    items = []
    launch("com.yacenkoea.pr6")
    shot(OUT / "pr6", "emu_form.png", "Форма ввода данных студента", items=items)
    tap_text("Имя")
    input_text("Ivan")
    tap_text("Фамилия")
    input_text("Petrov")
    tap_text("Группа")
    input_text("IST-21")
    tap_text("Возраст")
    input_text("20")
    tap_exact("Передать данные")
    time.sleep(0.8)
    shot(OUT / "pr6", "emu_result.png", "Вторая активность с данными, полученными через Intent", items=items)
    save(6, items)

    # 7
    install(7)
    items = []
    launch("com.yacenkoea.pr7")
    shot(OUT / "pr7", "emu_empty.png", "Первый экран до получения результата", items=items)
    tap_exact("Заполнить форму")
    time.sleep(0.6)
    shot(OUT / "pr7", "emu_form.png", "Второй экран с полем имени", items=items)
    tap_text("Введите имя")
    input_text("Alex")
    tap_exact("Сохранить")
    time.sleep(0.8)
    shot(OUT / "pr7", "emu_back.png", "Первый экран после возврата имени из второй активности", items=items)
    save(7, items)

    # 8
    install(8)
    items = []
    launch("com.yacenkoea.pr8")
    shot(OUT / "pr8", "emu_fit.png", "Изображение в режиме FIT_CENTER", items=items)
    tap_exact("CROP")
    shot(OUT / "pr8", "emu_crop.png", "Изображение в режиме CENTER_CROP", items=items)
    tap_exact("FILL")
    shot(OUT / "pr8", "emu_fill.png", "Изображение в режиме FIT_XY", items=items)
    save(8, items)

    # 9
    install(9)
    items = []
    launch("com.yacenkoea.pr9")
    shot(OUT / "pr9", "emu_idle.png", "Аудиоплеер до запуска: активна кнопка Play", items=items)
    tap_exact("Play")
    time.sleep(0.5)
    shot(OUT / "pr9", "emu_play.png", "Аудиоплеер во время воспроизведения: доступны Pause и Stop", items=items)
    save(9, items)

    # 10
    install(10)
    items = []
    launch("com.yacenkoea.pr10")
    time.sleep(1.0)
    tap_exact("Play")
    time.sleep(1.2)
    shot(OUT / "pr10", "emu_video.png", "VideoView во время воспроизведения локального ролика", items=items)
    save(10, items)

    # 11
    install(11)
    items = []
    launch("com.yacenkoea.pr11")
    shot(OUT / "pr11", "emu_frame.png", "Первый кадр анимации до запуска", items=items)
    tap_exact("Старт")
    time.sleep(0.7)
    shot(OUT / "pr11", "emu_run.png", "Кадровая анимация во время воспроизведения", items=items)
    save(11, items)

    # 12
    install(12)
    items = []
    launch("com.yacenkoea.pr12")
    shot(OUT / "pr12", "emu_still.png", "Изображение до запуска анимации", items=items)
    tap_exact("Вокруг центра")
    time.sleep(0.6)
    shot(OUT / "pr12", "emu_center.png", "Вращение вокруг центра изображения", items=items)
    tap_exact("Вокруг угла")
    time.sleep(0.6)
    shot(OUT / "pr12", "emu_corner.png", "Вращение вокруг левого верхнего угла", items=items)
    save(12, items)

    # 13
    install(13)
    items = []
    launch("com.yacenkoea.pr13")
    time.sleep(0.6)
    shot(OUT / "pr13", "emu_before.png", "Небо, трава и солнце до анимации", items=items)
    tap_exact("Восход")
    time.sleep(5.4)
    shot(OUT / "pr13", "emu_after.png", "Солнце после анимации восхода", items=items)
    save(13, items)

    # 14
    install(14)
    items = []
    launch("com.yacenkoea.pr14")
    time.sleep(0.8)
    shot(OUT / "pr14", "emu_list.png", "Список автомобилей, отсортированный по возрастанию цены", items=items)
    tap_exact("Все")
    time.sleep(0.4)
    tap_exact("Lada")
    time.sleep(0.6)
    shot(OUT / "pr14", "emu_filter.png", "Фильтр по производителю Lada", items=items)
    tap_exact("Добавить")
    time.sleep(0.8)
    shot(OUT / "pr14", "emu_form.png", "Форма добавления автомобиля", items=items)
    save(14, items)


if __name__ == "__main__":
    flow()
