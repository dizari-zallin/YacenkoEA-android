package com.yacenkoea.pr5;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

/** Второе окно. Кнопка возвращает на первый экран. */
public class AboutActivity extends AppCompatActivity {
    Button button;

    View.OnClickListener listener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            Intent intent = new Intent(AboutActivity.this, MainActivity.class);
            startActivity(intent);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
        button = findViewById(R.id.button);
        button.setOnClickListener(listener);
    }
}
