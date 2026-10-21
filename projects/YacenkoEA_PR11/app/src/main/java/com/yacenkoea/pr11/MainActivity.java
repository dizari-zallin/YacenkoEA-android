package com.yacenkoea.pr11;

import android.graphics.drawable.AnimationDrawable;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

/** Покадровая анимация: список кадров запускается и останавливается кнопками. */
public class MainActivity extends AppCompatActivity {
    ImageView imageView;
    AnimationDrawable animation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
        imageView.setBackgroundResource(R.drawable.animation);
        animation = (AnimationDrawable) imageView.getBackground();
    }

    public void startAnimation(View view) {
        if (animation != null && !animation.isRunning()) {
            animation.start();
        }
    }

    public void stopAnimation(View view) {
        if (animation != null && animation.isRunning()) {
            animation.stop();
        }
    }
}
