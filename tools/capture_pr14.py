# -*- coding: utf-8 -*-
import importlib.util
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "cap", Path(__file__).with_name("capture_emulator.py")
)
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)


def main():
    cap.install(14)
    items = []
    cap.launch("com.yacenkoea.pr14")
    time.sleep(1.0)
    cap.shot(
        cap.OUT / "pr14",
        "emu_list.png",
        "Список из 12 автомобилей, отсортированный по возрастанию цены",
        items=items,
    )
    cap.tap_exact("Все")
    time.sleep(0.5)
    cap.tap_exact("Lada")
    time.sleep(0.8)
    cap.shot(
        cap.OUT / "pr14",
        "emu_filter.png",
        "Список после фильтрации по производителю Lada",
        items=items,
    )
    cap.tap_exact("Добавить")
    time.sleep(1.0)
    cap.shot(
        cap.OUT / "pr14",
        "emu_form.png",
        "Форма добавления нового автомобиля",
        items=items,
    )
    cap.sh("input keyevent 4")
    time.sleep(0.6)
    cap.tap_text("Lada Vesta, 2021")
    time.sleep(0.8)
    cap.shot(
        cap.OUT / "pr14",
        "emu_edit.png",
        "Форма редактирования выбранного автомобиля",
        items=items,
    )
    cap.save(14, items)


if __name__ == "__main__":
    main()
