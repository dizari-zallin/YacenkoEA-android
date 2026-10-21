package com.yacenkoea.pr3;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

/** Экран со счётчиком нажатий на кнопку. */
public class MainActivity extends AppCompatActivity {
    TextView myTextView;
    Button myButton;

    /** Счётчик хранится в обработчике и увеличивается при каждом нажатии. */
    View.OnClickListener oMyButton = new View.OnClickListener() {
        int counter = 0;

        @Override
        public void onClick(View v) {
            myTextView.setText(String.valueOf(++counter));
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myTextView = findViewById(R.id.textView);
        myButton = findViewById(R.id.button);
        myButton.setOnClickListener(oMyButton);
    }
}
