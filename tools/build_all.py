# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\Shmurdyakich\Desktop\androidALL\projects")
GRADLE = Path(r"D:\androidALL\gradle-9.6.0\bin\gradle.bat")
JAVA = r"C:\Program Files\Android\Android Studio\jbr"
SDK = Path(os.environ["LOCALAPPDATA"]) / "Android" / "Sdk"


def main() -> int:
    env = os.environ.copy()
    env["JAVA_HOME"] = JAVA
    env["GRADLE_USER_HOME"] = r"D:\gradle-user-home"
    env["ANDROID_HOME"] = str(SDK)
    env["ANDROID_SDK_ROOT"] = str(SDK)
    projects = sorted(p for p in ROOT.iterdir() if p.is_dir())
    failed = []
    for project in projects:
        print("=== BUILD", project.name, flush=True)
        result = subprocess.run(
            [str(GRADLE), "assembleDebug", "--stacktrace"],
            cwd=project,
            env=env,
        )
        if result.returncode != 0:
            failed.append(project.name)
            print("FAILED", project.name, flush=True)
    print("FAILED:", failed or "none")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
