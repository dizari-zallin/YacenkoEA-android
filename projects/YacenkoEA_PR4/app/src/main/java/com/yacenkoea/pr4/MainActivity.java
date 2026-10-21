package com.yacenkoea.pr4;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

/** Экран, который берёт текст и цвета из файлов ресурсов. */
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Первая надпись получает строку напрямую по ссылке на ресурс.
        TextView firstView = findViewById(R.id.textView1);
        firstView.setText(R.string.message);

        // Вторая надпись читает ту же строку и цвета уже из кода.
        TextView codeView = findViewById(R.id.textViewCode);
        String message = getResources().getString(R.string.message);
        codeView.setText(message);
        int textColor = getResources().getColor(R.color.textViewFontColor, null);
        int backColor = getResources().getColor(R.color.textViewBackColor, null);
        codeView.setTextColor(textColor);
        codeView.setBackgroundColor(backColor);
    }
}
