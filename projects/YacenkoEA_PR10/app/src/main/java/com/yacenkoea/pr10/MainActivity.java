package com.yacenkoea.pr10;

import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.VideoView;
import androidx.appcompat.app.AppCompatActivity;

/** Проигрыватель видео: локальный ролик и ролик по адресу в сети. */
public class MainActivity extends AppCompatActivity {
    VideoView videoPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        videoPlayer = findViewById(R.id.videoPlayer);
        loadLocal();
    }

    /** Подставляет видеоклип из ресурсов приложения. */
    private void loadLocal() {
        String path = "android.resource://" + getPackageName() + "/" + R.raw.clip;
        videoPlayer.setVideoURI(Uri.parse(path));
    }

    public void play(View view) {
        videoPlayer.start();
    }

    public void pause(View view) {
        videoPlayer.pause();
    }

    public void stop(View view) {
        videoPlayer.stopPlayback();
        loadLocal();
    }

    /** Переключает плеер на ролик по HTTP-адресу. */
    public void playNetwork(View view) {
        videoPlayer.setVideoPath("http://techslides.com/demos/sample-videos/small.mp4");
        videoPlayer.start();
    }
}
