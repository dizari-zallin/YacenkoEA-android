# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "report", Path(__file__).with_name("make_report.py")
)
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)

split = report.ROOT / "Отчеты"
old = split / "Отчет_ПР14_Викторина.docx"
if old.exists():
    try:
        old.unlink()
        print("removed quiz report")
    except OSError as error:
        print("quiz report locked", error)

for lab in report.LABS:
    single = report.new_document()
    if lab["n"]:
        subtitle = f"по практической работе № {lab['n']}"
    else:
        subtitle = "по вводному занятию"
    report.add_title_page(single, [
        subtitle,
        "по дисциплине «Разработка мобильных приложений»",
    ])
    report.write_lab(single, lab)
    report.add_sources(single)
    path = split / report.SPLIT_NAMES[lab["n"]]
    try:
        single.save(path)
        print("saved", path.name)
    except PermissionError:
        print("LOCKED", path.name)
