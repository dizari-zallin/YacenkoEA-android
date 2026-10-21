# -*- coding: utf-8 -*-
"""Rename lab projects to YacenkoEA and switch the Java package."""
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\Shmurdyakich\Desktop\androidALL\projects")
TEXT_SUFFIXES = {".java", ".xml", ".gradle", ".properties", ".kts", ".txt", ".bat"}


def replace_text(path: Path, n: int) -> None:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return
    original = text
    text = text.replace(f"com.shmurdyakich.pr{n}", f"com.yacenkoea.pr{n}")
    text = text.replace(f"Shmurdyakich_PR{n}", f"YacenkoEA_PR{n}")
    text = text.replace(f"Shmurdyakich PR{n}", f"Яценко PR{n}")
    if n == 4 and 'name="app_name">ViewApp<' in text:
        text = text.replace('name="app_name">ViewApp<', 'name="app_name">Яценко PR4<')
    if text != original:
        path.write_text(text, encoding="utf-8")


def main() -> None:
    for n in range(1, 15):
        src = ROOT / f"Shmurdyakich_PR{n}"
        dst = ROOT / f"YacenkoEA_PR{n}"
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            src.rename(dst)
        if not dst.exists():
            raise SystemExit(f"missing {dst}")
        for junk in (dst / ".idea", dst / ".gradle"):
            if junk.exists():
                shutil.rmtree(junk)
        java_old = dst / "app" / "src" / "main" / "java" / "com" / "shmurdyakich" / f"pr{n}"
        java_new = dst / "app" / "src" / "main" / "java" / "com" / "yacenkoea" / f"pr{n}"
        if java_old.exists():
            java_new.parent.mkdir(parents=True, exist_ok=True)
            if java_new.exists():
                shutil.rmtree(java_new)
            java_old.rename(java_new)
        leftover = dst / "app" / "src" / "main" / "java" / "com" / "shmurdyakich"
        if leftover.exists():
            shutil.rmtree(leftover)
        for path in dst.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                replace_text(path, n)
        print(dst.name)


if __name__ == "__main__":
    main()
