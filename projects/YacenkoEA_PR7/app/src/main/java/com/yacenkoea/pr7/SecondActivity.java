package com.yacenkoea.pr7;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

/** Второй экран. Возвращает введённое имя на первый экран. */
public class SecondActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        EditText editText = findViewById(R.id.editText);
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String name = editText.getText().toString().trim();
                if (name.isEmpty()) {
                    editText.setError("Введите имя");
                    return;
                }
                // Результат кладётся в Intent и активность закрывается.
                Intent data = new Intent();
                data.putExtra("name", name);
                setResult(RESULT_OK, data);
                finish();
            }
        });
    }
}
