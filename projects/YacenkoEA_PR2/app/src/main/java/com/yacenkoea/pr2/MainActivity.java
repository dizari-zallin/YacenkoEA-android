package com.yacenkoea.pr2;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

/**
 * Экран с полем ввода, кнопкой, текстовой надписью и картинкой.
 * Картинка скрыта до нажатия кнопки.
 */
public class MainActivity extends AppCompatActivity {
    TextView myTextView;
    Button myButton;
    ImageButton imageButton;
    EditText editText;

    /** По нажатию показывает введённый текст и делает картинку видимой. */
    View.OnClickListener oMyButton = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            String entered = editText.getText().toString().trim();
            if (entered.isEmpty()) {
                myTextView.setText("Все ок)");
            } else {
                myTextView.setText(entered);
            }
            imageButton.setVisibility(View.VISIBLE);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Поиск элементов разметки и назначение обработчика кнопке.
        myTextView = findViewById(R.id.textView);
        myButton = findViewById(R.id.button);
        imageButton = findViewById(R.id.imageButton);
        editText = findViewById(R.id.editText);
        myButton.setOnClickListener(oMyButton);
    }
}
