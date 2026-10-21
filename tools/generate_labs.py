# -*- coding: utf-8 -*-
"""Generates Java/Android Studio projects for practical works 1-14."""
import os
import shutil
import struct
import wave
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\Shmurdyakich\Desktop\androidALL\projects")
SDK = Path(os.environ["LOCALAPPDATA"]) / "Android" / "Sdk"
LAUNCHER = SDK / "platforms" / "android-37.0" / "templates"
FFMPEG_JAR = Path(r"C:\Program Files\Android\Android Studio\plugins\android\lib\ffmpeg-7.1.1-1.5.12-windows-x86_64.jar")
FFMPEG_DIR = Path(r"D:\androidALL\ffmpeg")

AGP = "9.4.1"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8")


def project_gradle_files(folder: Path, name: str, pkg: str) -> None:
    write(folder / "settings.gradle", f"""\
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{name}"
include ':app'
""")
    write(folder / "build.gradle", f"""\
plugins {{
    id 'com.android.application' version '{AGP}' apply false
}}

layout.buildDirectory.set(file("D:/androidALL-build/{name}/root"))

subprojects {{
    layout.buildDirectory.set(file("D:/androidALL-build/{name}/${{project.name}}"))
}}
""")
    write(folder / "gradle.properties", """\
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
org.gradle.parallel=true
""")
    write(folder / "gradle/wrapper/gradle-wrapper.properties", """\
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-9.6.0-bin.zip
networkTimeout=60000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")
    write(folder / "local.properties", "sdk.dir=C:/Users/Shmurdyakich/AppData/Local/Android/Sdk\n")
    write(folder / "app/build.gradle", f"""\
plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{pkg}'
    compileSdk {{
        version = release(37) {{
            minorApiLevel = 0
        }}
    }}

    defaultConfig {{
        applicationId '{pkg}'
        minSdk 24
        targetSdk 37
        versionCode 1
        versionName "1.0"
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.7.1'
    implementation 'com.google.android.material:material:1.13.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.2.1'
    implementation 'androidx.activity:activity:1.10.1'
}}
""")
    write(folder / "app/proguard-rules.pro", "# Default proguard rules.\n")
    write(folder / "app/src/main/res/values/colors.xml", """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#1565C0</color>
    <color name="primary_dark">#0D47A1</color>
    <color name="accent">#EF6C00</color>
    <color name="white">#FFFFFF</color>
    <color name="black">#212121</color>
</resources>
""")
    write(folder / "app/src/main/res/values/themes.xml", """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.Lab" parent="Theme.AppCompat.Light.DarkActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/accent</item>
    </style>
</resources>
""")
    for density, src_name in (
        ("mipmap-mdpi", "ic_launcher_mdpi.png"),
        ("mipmap-hdpi", "ic_launcher_hdpi.png"),
        ("mipmap-xhdpi", "ic_launcher_xhdpi.png"),
    ):
        src = LAUNCHER / src_name
        dst = folder / "app/src/main/res" / density / "ic_launcher.png"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copyfile(src, dst)


def manifest(pkg_comment: str, app_activities, permissions=()) -> str:
    perms = "\n".join(f'    <uses-permission android:name="{p}" />' for p in permissions)
    if perms:
        perms = "\n" + perms
    acts = []
    for i, (cls, exported, launcher) in enumerate(app_activities):
        filt = ""
        if launcher:
            filt = """
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>"""
        acts.append(f"""        <activity
            android:name=".{cls}"
            android:exported="{str(exported).lower()}">{filt}
        </activity>""")
    body = "\n".join(acts)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">{perms}
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.Lab"
        android:usesCleartextTraffic="true">
{body}
    </application>
</manifest>
"""


def strings(app_name: str, extra="") -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
{extra}</resources>
"""


def java(pkg: str, filename: str, body: str) -> tuple:
    return filename, f"package {pkg};\n\n{body}"


# ---------- assets ----------

def make_picture(path: Path) -> None:
    img = Image.new("RGB", (320, 320), "#E3F2FD")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 180, 320, 320), fill="#66BB6A")
    d.ellipse((210, 30, 290, 110), fill="#FDD835")
    d.polygon([(40, 200), (120, 80), (200, 200)], fill="#2E7D32")
    d.polygon([(140, 210), (230, 110), (300, 210)], fill="#1B5E20")
    d.ellipse((70, 230, 130, 290), fill="#EF6C00")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG")


def make_sample(path: Path) -> None:
    img = Image.new("RGB", (480, 320), "#FFFFFF")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 160, 320), fill="#1565C0")
    d.rectangle((160, 0, 320, 160), fill="#EF6C00")
    d.rectangle((320, 0, 480, 320), fill="#2E7D32")
    d.ellipse((180, 180, 300, 300), fill="#C62828")
    d.rectangle((40, 40, 120, 120), fill="#FDD835")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG")


def make_figure(path: Path) -> None:
    img = Image.new("RGBA", (280, 280), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, 260, 260), radius=24, fill="#1565C0")
    d.polygon([(70, 200), (140, 60), (210, 200)], fill="#FDD835")
    d.ellipse((118, 150, 162, 194), fill="#C62828")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG")


def make_frames(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    colors = ["#1565C0", "#00838F", "#2E7D32", "#F9A825", "#EF6C00", "#C62828", "#6A1B9A", "#283593"]
    for i, color in enumerate(colors, start=1):
        img = Image.new("RGB", (280, 280), "#FFF8E1")
        d = ImageDraw.Draw(img)
        cx = 40 + i * 26
        cy = 180 - abs(i - 4) * 28
        d.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=color)
        d.rectangle((20, 230, 260, 250), fill="#81C784")
        img.save(folder / f"animation_{i}.png", "PNG")


def make_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fr = 22050
    notes = [262, 330, 392, 523, 392, 330, 262, 196]
    duration = 0.35
    amp = 12000
    frames = bytearray()
    for freq in notes:
        n = int(fr * duration)
        for i in range(n):
            # square-ish soft tone
            s = amp if (int(i * freq / fr * 2) % 2 == 0) else -amp
            env = 1.0
            if i < 200:
                env = i / 200
            if i > n - 400:
                env = max(0, (n - i) / 400)
            val = int(s * env * 0.7)
            frames += struct.pack("<h", val)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fr)
        w.writeframes(frames)


def ensure_ffmpeg() -> Path | None:
    exe = FFMPEG_DIR / "ffmpeg.exe"
    if exe.exists():
        return exe
    if not FFMPEG_JAR.exists():
        return None
    FFMPEG_DIR.mkdir(parents=True, exist_ok=True)
    prefix = "org/bytedeco/ffmpeg/windows-x86_64/"
    with zipfile.ZipFile(FFMPEG_JAR) as z:
        for info in z.infolist():
            if not info.filename.startswith(prefix):
                continue
            name = info.filename[len(prefix):]
            if not name or name.endswith("/"):
                continue
            if name.endswith(".dll") or name.endswith(".exe"):
                target = FFMPEG_DIR / name
                target.write_bytes(z.read(info))
    return exe if exe.exists() else None


def make_video(path: Path) -> None:
    ffmpeg = ensure_ffmpeg()
    frames = Path(r"D:\androidALL\video-frames")
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    colors = ["#C62828", "#EF6C00", "#F9A825", "#2E7D32", "#1565C0", "#6A1B9A"]
    for i, color in enumerate(colors):
        img = Image.new("RGB", (320, 240), color)
        d = ImageDraw.Draw(img)
        x = 20 + i * 40
        d.ellipse((x, 80, x + 70, 150), fill="#FFFFFF")
        img.save(frames / f"f{i:02d}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    if ffmpeg is None:
        # last resort: skip, caller checks
        return
    import subprocess
    subprocess.check_call([
        str(ffmpeg), "-y", "-framerate", "4",
        "-i", str(frames / "f%02d.png"),
        "-c:v", "mpeg4", "-q:v", "5", "-pix_fmt", "yuv420p",
        str(path),
    ])


# ---------- layouts ----------

HEADER = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="20dp">
"""
FOOTER = "</androidx.constraintlayout.widget.ConstraintLayout>\n"


def lab1():
    name, pkg = "Shmurdyakich_PR1", "com.shmurdyakich.pr1"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR1"))
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr1/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
""")


def lab2():
    name, pkg = "Shmurdyakich_PR2", "com.shmurdyakich.pr2"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR2"))
    make_picture(folder / "app/src/main/res/drawable/picture.png")
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <EditText
        android:id="@+id/editText"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:hint="Введите текст"
        android:inputType="text"
        android:minHeight="48dp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="12dp"
        android:text="Показать"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/editText" />

    <TextView
        android:id="@+id/textView"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="Текст появится здесь"
        android:textSize="20sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/button" />

    <ImageButton
        android:id="@+id/imageButton"
        android:layout_width="180dp"
        android:layout_height="180dp"
        android:layout_marginTop="16dp"
        android:background="#E3F2FD"
        android:contentDescription="Картинка"
        android:scaleType="fitCenter"
        android:src="@drawable/picture"
        android:visibility="invisible"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/textView" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr2/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    TextView myTextView;
    Button myButton;
    ImageButton imageButton;
    EditText editText;

    View.OnClickListener oMyButton = new View.OnClickListener() {{
        @Override
        public void onClick(View v) {{
            String entered = editText.getText().toString().trim();
            if (entered.isEmpty()) {{
                myTextView.setText("Все ок)");
            }} else {{
                myTextView.setText(entered);
            }}
            imageButton.setVisibility(View.VISIBLE);
        }}
    }};

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myTextView = findViewById(R.id.textView);
        myButton = findViewById(R.id.button);
        imageButton = findViewById(R.id.imageButton);
        editText = findViewById(R.id.editText);
        myButton.setOnClickListener(oMyButton);
    }}
}}
""")


def lab3():
    name, pkg = "Shmurdyakich_PR3", "com.shmurdyakich.pr3"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR3"))
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="0"
        android:textSize="48sp"
        app:layout_constraintBottom_toTopOf="@id/button"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="Нажми меня"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/textView" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr3/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    TextView myTextView;
    Button myButton;

    View.OnClickListener oMyButton = new View.OnClickListener() {{
        int counter = 0;

        @Override
        public void onClick(View v) {{
            myTextView.setText(String.valueOf(++counter));
        }}
    }};

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myTextView = findViewById(R.id.textView);
        myButton = findViewById(R.id.button);
        myButton.setOnClickListener(oMyButton);
    }}
}}
""")


def lab4():
    name, pkg = "Shmurdyakich_PR4", "com.shmurdyakich.pr4"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">ViewApp</string>
    <string name="message">Hello Android!</string>
</resources>
""")
    write(folder / "app/src/main/res/values/headers.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="main_header">Строковые ресурсы</string>
    <string name="second_header">Цветовые ресурсы</string>
</resources>
""")
    write(folder / "app/src/main/res/values/my_colors.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="textViewFontColor">#0D47A1</color>
    <color name="textViewBackColor">#BBDEFB</color>
    <color name="headerFontColor">#B71C1C</color>
    <color name="screenBackground">#FFFDE7</color>
</resources>
""")
    write(folder / "app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/screenBackground"
    android:padding="20dp">

    <TextView
        android:id="@+id/headerView"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="@string/main_header"
        android:textColor="@color/headerFontColor"
        android:textSize="22sp"
        android:textStyle="bold"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <TextView
        android:id="@+id/textView1"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:background="@color/textViewBackColor"
        android:gravity="center"
        android:padding="16dp"
        android:text="@string/message"
        android:textColor="@color/textViewFontColor"
        android:textSize="20sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/headerView" />

    <TextView
        android:id="@+id/textViewCode"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:gravity="center"
        android:padding="16dp"
        android:text="@string/second_header"
        android:textSize="18sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/textView1" />
</androidx.constraintlayout.widget.ConstraintLayout>
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr4/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView firstView = findViewById(R.id.textView1);
        firstView.setText(R.string.message);

        TextView codeView = findViewById(R.id.textViewCode);
        String message = getResources().getString(R.string.message);
        codeView.setText(message);
        int textColor = getResources().getColor(R.color.textViewFontColor, null);
        int backColor = getResources().getColor(R.color.textViewBackColor, null);
        codeView.setTextColor(textColor);
        codeView.setBackgroundColor(backColor);
    }}
}}
""")


def lab5():
    name, pkg = "Shmurdyakich_PR5", "com.shmurdyakich.pr5"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [
        ("MainActivity", True, True),
        ("AboutActivity", False, False),
    ]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR5"))
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Первое окно"
        android:textSize="28sp"
        app:layout_constraintBottom_toTopOf="@id/button"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="Открыть второе окно"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/textView" />
""" + FOOTER)
    write(folder / "app/src/main/res/layout/activity_about.xml", HEADER + """
    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Второе окно"
        android:textSize="28sp"
        app:layout_constraintBottom_toTopOf="@id/button"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="Вернуться в первое окно"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/textView" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr5/MainActivity.java", f"""package {pkg};

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    Button button;

    View.OnClickListener listener = new View.OnClickListener() {{
        @Override
        public void onClick(View v) {{
            Intent intent = new Intent(MainActivity.this, AboutActivity.class);
            startActivity(intent);
        }}
    }};

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        button = findViewById(R.id.button);
        button.setOnClickListener(listener);
    }}
}}
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr5/AboutActivity.java", f"""package {pkg};

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class AboutActivity extends AppCompatActivity {{
    Button button;

    View.OnClickListener listener = new View.OnClickListener() {{
        @Override
        public void onClick(View v) {{
            Intent intent = new Intent(AboutActivity.this, MainActivity.class);
            startActivity(intent);
        }}
    }};

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
        button = findViewById(R.id.button);
        button.setOnClickListener(listener);
    }}
}}
""")


def lab6():
    name, pkg = "Shmurdyakich_PR6", "com.shmurdyakich.pr6"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [
        ("MainActivity", True, True),
        ("SecondActivity", False, False),
    ]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR6"))
    write(folder / "app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="20dp">

        <EditText
            android:id="@+id/editTextText2"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Имя"
            android:inputType="textPersonName"
            android:minHeight="48dp" />

        <EditText
            android:id="@+id/editTextText5"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:hint="Фамилия"
            android:inputType="textPersonName"
            android:minHeight="48dp" />

        <EditText
            android:id="@+id/editTextText3"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:hint="Группа"
            android:inputType="text"
            android:minHeight="48dp" />

        <EditText
            android:id="@+id/editTextText4"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:hint="Возраст"
            android:inputType="number"
            android:minHeight="48dp" />

        <Button
            android:id="@+id/button"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:text="Передать данные" />
    </LinearLayout>
</ScrollView>
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr6/Human.java", f"""package {pkg};

import java.io.Serializable;

public abstract class Human implements Serializable {{
    protected String firstName;
    protected String lastName;
    protected Integer age;

    Human() {{
    }}

    Human(String name) {{
        this.firstName = name;
    }}

    Human(String name, String lastName) {{
        this.firstName = name;
        this.lastName = lastName;
    }}

    Human(String name, String lastName, Integer age) {{
        this.firstName = name;
        this.lastName = lastName;
        this.age = age;
    }}

    public String getFirstName() {{
        return firstName;
    }}

    public String getLastName() {{
        return lastName;
    }}

    public Integer getAge() {{
        return age;
    }}

    public void setFirstName(String firstName) {{
        this.firstName = firstName;
    }}

    public void setLastName(String lastName) {{
        this.lastName = lastName;
    }}

    public void setAge(Integer age) {{
        this.age = age;
    }}

    public String toString() {{
        return String.format("Human = {{firstName: %s, lastName: %s, age: %d}}",
                this.firstName, this.lastName, this.age);
    }}
}}
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr6/Student.java", f"""package {pkg};

public class Student extends Human {{
    private String group;

    Student() {{
    }}

    public Student(String name, String group) {{
        super(name);
        this.group = group;
    }}

    public Student(String name, String lastName, String group) {{
        super(name, lastName);
        this.group = group;
    }}

    public Student(String name, String lastName, Integer age, String group) {{
        super(name, lastName, age);
        this.group = group;
    }}

    public String getGroup() {{
        return group;
    }}

    public void setGroup(String group) {{
        this.group = group;
    }}

    @Override
    public String toString() {{
        return String.format("Human = {{firstName: %s, lastName: %s, age: %d, group: %s}}",
                this.firstName, this.lastName, this.age, this.group);
    }}
}}
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr6/MainActivity.java", f"""package {pkg};

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    EditText firstNameText;
    EditText secondNameText;
    EditText groupText;
    EditText ageText;
    Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        firstNameText = findViewById(R.id.editTextText2);
        secondNameText = findViewById(R.id.editTextText5);
        groupText = findViewById(R.id.editTextText3);
        ageText = findViewById(R.id.editTextText4);
        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                String firstName = firstNameText.getText().toString();
                String secondName = secondNameText.getText().toString();
                String group = groupText.getText().toString();
                int age;
                try {{
                    age = Integer.parseInt(ageText.getText().toString().trim());
                }} catch (NumberFormatException ex) {{
                    ageText.setError("Введите число");
                    return;
                }}
                Student student1 = new Student(firstName, secondName, age, group);
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                intent.putExtra(Student.class.getSimpleName(), student1);
                startActivity(intent);
            }}
        }});
    }}
}}
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr6/SecondActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class SecondActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        TextView textView = new TextView(this);
        textView.setTextSize(26);
        textView.setPadding(32, 48, 32, 32);
        Bundle arguments = getIntent().getExtras();
        if (arguments != null) {{
            Student student1 = (Student) arguments.getSerializable(Student.class.getSimpleName());
            if (student1 != null) {{
                textView.setText("Имя: " + student1.getFirstName() + " "
                        + student1.getLastName()
                        + "\\nГруппа: "
                        + student1.getGroup()
                        + "\\nВозраст: " + student1.getAge());
            }}
        }}
        setContentView(textView);
    }}
}}
""")


def lab7():
    name, pkg = "Shmurdyakich_PR7", "com.shmurdyakich.pr7"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [
        ("MainActivity", True, True),
        ("SecondActivity", False, False),
    ]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR7"))
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <TextView
        android:id="@+id/textView"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="Имя не задано"
        android:textSize="24sp"
        app:layout_constraintBottom_toTopOf="@id/button"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="Заполнить форму"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/textView" />
""" + FOOTER)
    write(folder / "app/src/main/res/layout/activity_second.xml", HEADER + """
    <EditText
        android:id="@+id/editText"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:hint="Введите имя"
        android:inputType="textPersonName"
        android:minHeight="48dp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="Сохранить"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/editText" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr7/MainActivity.java", f"""package {pkg};

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    TextView textView;
    ActivityResultLauncher<Intent> mStartForResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        mStartForResult = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                new ActivityResultCallback<ActivityResult>() {{
                    @Override
                    public void onActivityResult(ActivityResult result) {{
                        if (result.getResultCode() == RESULT_OK && result.getData() != null) {{
                            String name = result.getData().getStringExtra("name");
                            textView.setText("Имя: " + name);
                        }}
                    }}
                }});
        setContentView(R.layout.activity_main);
        textView = findViewById(R.id.textView);
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                mStartForResult.launch(intent);
            }}
        }});
    }}
}}
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr7/SecondActivity.java", f"""package {pkg};

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

public class SecondActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        EditText editText = findViewById(R.id.editText);
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                String name = editText.getText().toString().trim();
                if (name.isEmpty()) {{
                    editText.setError("Введите имя");
                    return;
                }}
                Intent data = new Intent();
                data.putExtra("name", name);
                setResult(RESULT_OK, data);
                finish();
            }}
        }});
    }}
}}
""")


def lab8():
    name, pkg = "Shmurdyakich_PR8", "com.shmurdyakich.pr8"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR8"))
    make_sample(folder / "app/src/main/res/drawable/sample.png")
    write(folder / "app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="12dp">

    <TextView
        android:id="@+id/scaleLabel"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="Масштаб: FIT_CENTER"
        android:textSize="16sp" />

    <ImageView
        android:id="@+id/imageView"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_marginTop="8dp"
        android:layout_weight="1"
        android:background="#EEEEEE"
        android:contentDescription="Изображение"
        android:scaleType="fitCenter"
        android:src="@drawable/sample" />

    <HorizontalScrollView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp">

        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="horizontal">

            <Button
                android:id="@+id/button"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Галерея" />

            <Button
                android:id="@+id/btnCenter"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="CENTER" />

            <Button
                android:id="@+id/btnCrop"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="CROP" />

            <Button
                android:id="@+id/btnInside"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="INSIDE" />

            <Button
                android:id="@+id/btnFit"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="FIT" />

            <Button
                android:id="@+id/btnFill"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="FILL" />
        </LinearLayout>
    </HorizontalScrollView>
</LinearLayout>
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr8/MainActivity.java", f"""package {pkg};

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity {{
    static final int GALLERY_REQUEST = 1;
    ImageView imageView;
    TextView scaleLabel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
        scaleLabel = findViewById(R.id.scaleLabel);
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                Intent photoPickerIntent = new Intent(Intent.ACTION_PICK);
                photoPickerIntent.setType("image/*");
                startActivityForResult(photoPickerIntent, GALLERY_REQUEST);
            }}
        }});
        findViewById(R.id.btnCenter).setOnClickListener(v -> applyScale(ImageView.ScaleType.CENTER, "CENTER"));
        findViewById(R.id.btnCrop).setOnClickListener(v -> applyScale(ImageView.ScaleType.CENTER_CROP, "CENTER_CROP"));
        findViewById(R.id.btnInside).setOnClickListener(v -> applyScale(ImageView.ScaleType.CENTER_INSIDE, "CENTER_INSIDE"));
        findViewById(R.id.btnFit).setOnClickListener(v -> applyScale(ImageView.ScaleType.FIT_CENTER, "FIT_CENTER"));
        findViewById(R.id.btnFill).setOnClickListener(v -> applyScale(ImageView.ScaleType.FIT_XY, "FIT_XY"));
    }}

    private void applyScale(ImageView.ScaleType type, String name) {{
        imageView.setScaleType(type);
        scaleLabel.setText("Масштаб: " + name);
    }}

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent) {{
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent);
        if (requestCode == GALLERY_REQUEST && resultCode == RESULT_OK && imageReturnedIntent != null) {{
            Uri selectedImage = imageReturnedIntent.getData();
            if (selectedImage == null) {{
                return;
            }}
            try (InputStream stream = getContentResolver().openInputStream(selectedImage)) {{
                Bitmap bitmap = BitmapFactory.decodeStream(stream);
                imageView.setImageBitmap(bitmap);
            }} catch (IOException e) {{
                e.printStackTrace();
            }}
        }}
    }}
}}
""")


def lab9():
    name, pkg = "Shmurdyakich_PR9", "com.shmurdyakich.pr9"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)], [
        "android.permission.MODIFY_AUDIO_SETTINGS"
    ]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR9"))
    make_wav(folder / "app/src/main/res/raw/music.wav")
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <TextView
        android:id="@+id/title"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="Аудиоплеер"
        android:textSize="24sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/playButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:onClick="play"
        android:text="Play"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/title" />

    <Button
        android:id="@+id/pauseButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:onClick="pause"
        android:text="Pause"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/playButton" />

    <Button
        android:id="@+id/stopButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:onClick="stop"
        android:text="Stop"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/pauseButton" />

    <SeekBar
        android:id="@+id/volumeControl"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="32dp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/stopButton" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr9/MainActivity.java", f"""package {pkg};

import android.content.Context;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    MediaPlayer mPlayer;
    Button playButton, pauseButton, stopButton;
    SeekBar volumeControl;
    AudioManager audioManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mPlayer = MediaPlayer.create(this, R.raw.music);
        mPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {{
            @Override
            public void onCompletion(MediaPlayer mp) {{
                stopPlay();
            }}
        }});
        playButton = findViewById(R.id.playButton);
        pauseButton = findViewById(R.id.pauseButton);
        stopButton = findViewById(R.id.stopButton);
        pauseButton.setEnabled(false);
        stopButton.setEnabled(false);

        audioManager = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
        int maxVolume = audioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC);
        int curValue = audioManager.getStreamVolume(AudioManager.STREAM_MUSIC);
        volumeControl = findViewById(R.id.volumeControl);
        volumeControl.setMax(maxVolume);
        volumeControl.setProgress(curValue);
        volumeControl.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {{
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {{
                audioManager.setStreamVolume(AudioManager.STREAM_MUSIC, progress, 0);
            }}

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {{
            }}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {{
            }}
        }});
    }}

    private void stopPlay() {{
        mPlayer.stop();
        pauseButton.setEnabled(false);
        stopButton.setEnabled(false);
        try {{
            mPlayer.prepare();
            mPlayer.seekTo(0);
            playButton.setEnabled(true);
        }} catch (Throwable t) {{
            Toast.makeText(this, t.getMessage(), Toast.LENGTH_SHORT).show();
        }}
    }}

    public void play(View view) {{
        mPlayer.start();
        playButton.setEnabled(false);
        pauseButton.setEnabled(true);
        stopButton.setEnabled(true);
    }}

    public void pause(View view) {{
        mPlayer.pause();
        playButton.setEnabled(true);
        pauseButton.setEnabled(false);
        stopButton.setEnabled(true);
    }}

    public void stop(View view) {{
        stopPlay();
    }}

    @Override
    public void onDestroy() {{
        super.onDestroy();
        if (mPlayer != null) {{
            if (mPlayer.isPlaying()) {{
                mPlayer.stop();
            }}
            mPlayer.release();
        }}
    }}
}}
""")


def lab10():
    name, pkg = "Shmurdyakich_PR10", "com.shmurdyakich.pr10"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)], [
        "android.permission.INTERNET"
    ]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR10"))
    make_video(folder / "app/src/main/res/raw/clip.mp4")
    write(folder / "app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="12dp">

    <VideoView
        android:id="@+id/videoPlayer"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

    <Button
        android:id="@+id/playButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:onClick="play"
        android:text="Play" />

    <Button
        android:id="@+id/pauseButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:onClick="pause"
        android:text="Pause" />

    <Button
        android:id="@+id/stopButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:onClick="stop"
        android:text="Stop" />

    <Button
        android:id="@+id/netButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:onClick="playNetwork"
        android:text="Из интернета" />
</LinearLayout>
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr10/MainActivity.java", f"""package {pkg};

import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.VideoView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    VideoView videoPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        videoPlayer = findViewById(R.id.videoPlayer);
        loadLocal();
    }}

    private void loadLocal() {{
        String path = "android.resource://" + getPackageName() + "/" + R.raw.clip;
        videoPlayer.setVideoURI(Uri.parse(path));
    }}

    public void play(View view) {{
        videoPlayer.start();
    }}

    public void pause(View view) {{
        videoPlayer.pause();
    }}

    public void stop(View view) {{
        videoPlayer.stopPlayback();
        loadLocal();
    }}

    public void playNetwork(View view) {{
        videoPlayer.setVideoPath("http://techslides.com/demos/sample-videos/small.mp4");
        videoPlayer.start();
    }}
}}
""")


def lab11():
    name, pkg = "Shmurdyakich_PR11", "com.shmurdyakich.pr11"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR11"))
    make_frames(folder / "app/src/main/res/drawable")
    items = "\n".join(
        f'    <item android:drawable="@drawable/animation_{i}" android:duration="180" />'
        for i in range(1, 9)
    )
    write(folder / "app/src/main/res/drawable/animation.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<animation-list xmlns:android="http://schemas.android.com/apk/res/android"
    android:oneshot="false">
{items}
</animation-list>
""")
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <ImageView
        android:id="@+id/imageView"
        android:layout_width="280dp"
        android:layout_height="280dp"
        android:contentDescription="Кадровая анимация"
        app:layout_constraintBottom_toTopOf="@id/startButton"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/startButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:onClick="startAnimation"
        android:text="Старт"
        app:layout_constraintBottom_toTopOf="@id/stopButton"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/stopButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:onClick="stopAnimation"
        android:text="Стоп"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr11/MainActivity.java", f"""package {pkg};

import android.graphics.drawable.AnimationDrawable;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    ImageView imageView;
    AnimationDrawable animation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
        imageView.setBackgroundResource(R.drawable.animation);
        animation = (AnimationDrawable) imageView.getBackground();
    }}

    public void startAnimation(View view) {{
        if (animation != null && !animation.isRunning()) {{
            animation.start();
        }}
    }}

    public void stopAnimation(View view) {{
        if (animation != null && animation.isRunning()) {{
            animation.stop();
        }}
    }}
}}
""")


def lab12():
    name, pkg = "Shmurdyakich_PR12", "com.shmurdyakich.pr12"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR12"))
    make_figure(folder / "app/src/main/res/drawable/figure.png")
    write(folder / "app/src/main/res/anim/rotate_center.xml", """<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
    android:interpolator="@android:anim/linear_interpolator">
    <rotate
        android:duration="3000"
        android:fromDegrees="0"
        android:pivotX="50%"
        android:pivotY="50%"
        android:repeatCount="infinite"
        android:toDegrees="360" />
</set>
""")
    write(folder / "app/src/main/res/anim/rotate_corner.xml", """<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
    android:interpolator="@android:anim/linear_interpolator">
    <rotate
        android:duration="3000"
        android:fromDegrees="0"
        android:pivotX="0%"
        android:pivotY="0%"
        android:repeatCount="infinite"
        android:toDegrees="360" />
</set>
""")
    write(folder / "app/src/main/res/layout/activity_main.xml", HEADER + """
    <ImageView
        android:id="@+id/imageView"
        android:layout_width="180dp"
        android:layout_height="180dp"
        android:contentDescription="Фигура"
        android:src="@drawable/figure"
        app:layout_constraintBottom_toTopOf="@id/centerButton"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/centerButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:onClick="rotateCenter"
        android:text="Вокруг центра"
        app:layout_constraintBottom_toTopOf="@id/cornerButton"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/cornerButton"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:onClick="rotateCorner"
        android:text="Вокруг угла"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />
""" + FOOTER)
    write(folder / "app/src/main/java/com/shmurdyakich/pr12/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
    }}

    public void rotateCenter(View view) {{
        Animation animation = AnimationUtils.loadAnimation(this, R.anim.rotate_center);
        imageView.startAnimation(animation);
    }}

    public void rotateCorner(View view) {{
        Animation animation = AnimationUtils.loadAnimation(this, R.anim.rotate_corner);
        imageView.startAnimation(animation);
    }}
}}
""")


def lab13():
    name, pkg = "Shmurdyakich_PR13", "com.shmurdyakich.pr13"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR13", """    <string name="sunrise">Восход</string>
    <string name="sun_desc">Солнце</string>
    <string name="sky_desc">Небо</string>
    <string name="grass_desc">Трава</string>
"""))
    write(folder / "app/src/main/res/drawable/sun.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="oval">
    <size
        android:width="80dp"
        android:height="80dp" />
    <gradient
        android:endColor="#FFEB3B"
        android:gradientRadius="40dp"
        android:startColor="#FF8F00"
        android:type="radial" />
</shape>
""")
    write(folder / "app/src/main/res/drawable/sky.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:angle="90"
        android:endColor="#01579B"
        android:startColor="#81D4FA" />
</shape>
""")
    write(folder / "app/src/main/res/drawable/grass.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:angle="90"
        android:endColor="#66BB6A"
        android:startColor="#1B5E20" />
</shape>
""")
    write(folder / "app/src/main/res/anim/sun_rise.xml", """<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
    android:duration="5000"
    android:fillAfter="true"
    android:interpolator="@android:anim/accelerate_decelerate_interpolator">
    <scale
        android:fromXScale="1.0"
        android:fromYScale="1.0"
        android:pivotX="50%"
        android:pivotY="50%"
        android:toXScale="1.5"
        android:toYScale="1.5" />
    <translate
        android:fromYDelta="40%p"
        android:toYDelta="-35%p" />
    <alpha
        android:fromAlpha="0.3"
        android:toAlpha="1.0" />
</set>
""")
    write(folder / "app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/sky"
        android:layout_width="0dp"
        android:layout_height="0dp"
        android:contentDescription="@string/sky_desc"
        android:scaleType="fitXY"
        android:src="@drawable/sky"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <ImageView
        android:id="@+id/grass"
        android:layout_width="0dp"
        android:layout_height="160dp"
        android:contentDescription="@string/grass_desc"
        android:scaleType="fitXY"
        android:src="@drawable/grass"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />

    <ImageView
        android:id="@+id/sun"
        android:layout_width="90dp"
        android:layout_height="90dp"
        android:layout_marginBottom="24dp"
        android:contentDescription="@string/sun_desc"
        android:src="@drawable/sun"
        app:layout_constraintBottom_toTopOf="@id/grass"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:onClick="rise"
        android:text="@string/sunrise"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr13/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    ImageView sun;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        sun = findViewById(R.id.sun);
    }}

    public void rise(View view) {{
        Animation animation = AnimationUtils.loadAnimation(this, R.anim.sun_rise);
        sun.startAnimation(animation);
    }}
}}
""")


def lab14():
    name, pkg = "Shmurdyakich_PR14", "com.shmurdyakich.pr14"
    folder = ROOT / name
    project_gradle_files(folder, name, pkg)
    write(folder / "app/src/main/AndroidManifest.xml", manifest("", [("MainActivity", True, True)]))
    write(folder / "app/src/main/res/values/strings.xml", strings("Shmurdyakich PR14"))
    write(folder / "app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/progressView"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Вопрос 1 из 5"
        android:textSize="16sp" />

    <TextView
        android:id="@+id/questionView"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="12dp"
        android:textSize="20sp" />

    <Button
        android:id="@+id/option1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp" />

    <Button
        android:id="@+id/option2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <Button
        android:id="@+id/option3"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <Button
        android:id="@+id/option4"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <TextView
        android:id="@+id/resultView"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:textSize="22sp"
        android:visibility="gone" />
</LinearLayout>
""")
    write(folder / "app/src/main/java/com/shmurdyakich/pr14/MainActivity.java", f"""package {pkg};

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    private static final String[] QUESTIONS = new String[]{{
            "Как называется официальная среда разработки приложений для Android?",
            "Какой компонент соответствует одному экрану приложения?",
            "В каком файле объявляются компоненты приложения?",
            "Какой объект используется для передачи данных между экранами?",
            "Какой класс отвечает за воспроизведение аудио?"
    }};
    private static final String[][] OPTIONS = new String[][]{{
            {{"Android Studio", "Xcode", "Blender", "Excel"}},
            {{"Gradle", "Activity", "Drawable", "Manifest"}},
            {{"strings.xml", "MainActivity.java", "AndroidManifest.xml", "colors.xml"}},
            {{"TextView", "Intent", "Bitmap", "SeekBar"}},
            {{"VideoView", "ImageView", "MediaPlayer", "AnimationDrawable"}}
    }};
    private static final int[] ANSWERS = new int[]{{0, 1, 2, 1, 2}};

    private TextView progressView;
    private TextView questionView;
    private TextView resultView;
    private Button[] optionButtons;
    private int index;
    private int score;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        progressView = findViewById(R.id.progressView);
        questionView = findViewById(R.id.questionView);
        resultView = findViewById(R.id.resultView);
        optionButtons = new Button[]{{
                findViewById(R.id.option1),
                findViewById(R.id.option2),
                findViewById(R.id.option3),
                findViewById(R.id.option4)
        }};
        for (int i = 0; i < optionButtons.length; i++) {{
            final int choice = i;
            optionButtons[i].setOnClickListener(new View.OnClickListener() {{
                @Override
                public void onClick(View v) {{
                    onAnswer(choice);
                }}
            }});
        }}
        showQuestion();
    }}

    private void showQuestion() {{
        progressView.setText("Вопрос " + (index + 1) + " из " + QUESTIONS.length);
        questionView.setText(QUESTIONS[index]);
        for (int i = 0; i < optionButtons.length; i++) {{
            optionButtons[i].setText(OPTIONS[index][i]);
        }}
    }}

    private void onAnswer(int choice) {{
        if (choice == ANSWERS[index]) {{
            score++;
        }}
        index++;
        if (index >= QUESTIONS.length) {{
            showResult();
        }} else {{
            showQuestion();
        }}
    }}

    private void showResult() {{
        questionView.setVisibility(View.GONE);
        progressView.setText("Викторина завершена");
        for (Button button : optionButtons) {{
            button.setVisibility(View.GONE);
        }}
        resultView.setVisibility(View.VISIBLE);
        resultView.setText("Результат: " + score + " из " + QUESTIONS.length);
        optionButtons[0].setVisibility(View.VISIBLE);
        optionButtons[0].setText("Начать заново");
        optionButtons[0].setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                index = 0;
                score = 0;
                questionView.setVisibility(View.VISIBLE);
                resultView.setVisibility(View.GONE);
                for (int i = 0; i < optionButtons.length; i++) {{
                    optionButtons[i].setVisibility(View.VISIBLE);
                    final int choice = i;
                    optionButtons[i].setOnClickListener(new View.OnClickListener() {{
                        @Override
                        public void onClick(View view) {{
                            onAnswer(choice);
                        }}
                    }});
                }}
                showQuestion();
            }}
        }});
    }}
}}
""")


def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True)
    lab1()
    lab2()
    lab3()
    lab4()
    lab5()
    lab6()
    lab7()
    lab8()
    lab9()
    print("video...")
    lab10()
    lab11()
    lab12()
    lab13()
    lab14()
    print("projects:", ROOT)


if __name__ == "__main__":
    main()
