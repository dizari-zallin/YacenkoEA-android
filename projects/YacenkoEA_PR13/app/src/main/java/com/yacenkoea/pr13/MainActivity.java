package com.yacenkoea.pr13;

import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

/** Экран с небом, травой и солнцем. Кнопка запускает восход. */
public class MainActivity extends AppCompatActivity {
    ImageView sun;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        sun = findViewById(R.id.sun);
    }

    public void rise(View view) {
        Animation animation = AnimationUtils.loadAnimation(this, R.anim.sun_rise);
        sun.startAnimation(animation);
    }
}
