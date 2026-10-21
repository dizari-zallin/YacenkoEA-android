package com.yacenkoea.pr6;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

/** Форма анкеты студента. По кнопке данные уходят на второй экран. */
public class MainActivity extends AppCompatActivity {
    EditText firstNameText;
    EditText secondNameText;
    EditText groupText;
    EditText ageText;
    Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        firstNameText = findViewById(R.id.editTextText2);
        secondNameText = findViewById(R.id.editTextText5);
        groupText = findViewById(R.id.editTextText3);
        ageText = findViewById(R.id.editTextText4);
        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Сбор полей формы. Возраст должен быть числом.
                String firstName = firstNameText.getText().toString();
                String secondName = secondNameText.getText().toString();
                String group = groupText.getText().toString();
                int age;
                try {
                    age = Integer.parseInt(ageText.getText().toString().trim());
                } catch (NumberFormatException ex) {
                    ageText.setError("Введите число");
                    return;
                }
                Student student1 = new Student(firstName, secondName, age, group);
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                intent.putExtra(Student.class.getSimpleName(), student1);
                startActivity(intent);
            }
        });
    }
}
