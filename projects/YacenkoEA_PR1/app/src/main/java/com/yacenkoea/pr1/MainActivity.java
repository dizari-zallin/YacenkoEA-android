package com.yacenkoea.pr1;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

/**
 * Главный экран приложения. Показывает разметку с надписью Hello World!
 */
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Подключение XML-разметки activity_main.
        setContentView(R.layout.activity_main);
    }
}
