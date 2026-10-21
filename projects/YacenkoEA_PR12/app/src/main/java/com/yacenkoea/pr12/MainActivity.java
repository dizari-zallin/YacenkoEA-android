package com.yacenkoea.pr12;

import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

/** Вращение фигуры вокруг центра или вокруг левого верхнего угла. */
public class MainActivity extends AppCompatActivity {
    ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
    }

    public void rotateCenter(View view) {
        Animation animation = AnimationUtils.loadAnimation(this, R.anim.rotate_center);
        imageView.startAnimation(animation);
    }

    public void rotateCorner(View view) {
        Animation animation = AnimationUtils.loadAnimation(this, R.anim.rotate_corner);
        imageView.startAnimation(animation);
    }
}
