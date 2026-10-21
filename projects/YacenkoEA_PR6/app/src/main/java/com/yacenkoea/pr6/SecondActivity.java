package com.yacenkoea.pr6;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

/** Второй экран показывает данные студента, полученные из Intent. */
public class SecondActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView textView = new TextView(this);
        textView.setTextSize(26);
        textView.setPadding(32, 48, 32, 32);
        Bundle arguments = getIntent().getExtras();
        if (arguments != null) {
            Student student1 = (Student) arguments.getSerializable(Student.class.getSimpleName());
            if (student1 != null) {
                textView.setText("Имя: " + student1.getFirstName() + " "
                        + student1.getLastName()
                        + "\nГруппа: "
                        + student1.getGroup()
                        + "\nВозраст: " + student1.getAge());
            }
        }
        setContentView(textView);
    }
}
