package com.yacenkoea.pr14;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.List;

/** Форма нового автомобиля или редактирования уже существующей записи. */
public class CarActivity extends AppCompatActivity {
    private CarDbHelper database;
    private Spinner manufacturerSpinner;
    private Spinner modelSpinner;
    private EditText yearText;
    private EditText colorText;
    private EditText engineText;
    private EditText priceText;
    private long carId = -1;
    private String shownManufacturer = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car);
        database = new CarDbHelper(this);
        manufacturerSpinner = findViewById(R.id.manufacturerSpinner);
        modelSpinner = findViewById(R.id.modelSpinner);
        yearText = findViewById(R.id.yearText);
        colorText = findViewById(R.id.colorText);
        engineText = findViewById(R.id.engineText);
        priceText = findViewById(R.id.priceText);

        List<String> manufacturers = new ArrayList<>(CarDbHelper.CATALOG.keySet());
        manufacturerSpinner.setAdapter(new ArrayAdapter<>(
                this, android.R.layout.simple_spinner_dropdown_item, manufacturers));
        manufacturerSpinner.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(android.widget.AdapterView<?> parent, View view, int position, long id) {
                String manufacturer = parent.getItemAtPosition(position).toString();
                if (manufacturer.equals(shownManufacturer)) {
                    return;
                }
                shownManufacturer = manufacturer;
                fillModels(null);
            }

            @Override
            public void onNothingSelected(android.widget.AdapterView<?> parent) {
            }
        });

        carId = getIntent().getLongExtra(MainActivity.EXTRA_ID, -1);
        if (carId > 0) {
            setTitle("Редактирование");
            show(database.find(carId));
        } else {
            setTitle("Новый автомобиль");
            fillModels(null);
        }

        Button saveButton = findViewById(R.id.saveButton);
        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                save();
            }
        });
    }

    /** Подставляет марки выбранного производителя и, при редактировании, отмечает текущую. */
    private void fillModels(String selectedModel) {
        String manufacturer = manufacturerSpinner.getSelectedItem().toString();
        shownManufacturer = manufacturer;
        String[] models = CarDbHelper.CATALOG.get(manufacturer);
        modelSpinner.setAdapter(new ArrayAdapter<>(
                this, android.R.layout.simple_spinner_dropdown_item, models));
        if (selectedModel != null) {
            for (int i = 0; i < models.length; i++) {
                if (models[i].equals(selectedModel)) {
                    modelSpinner.setSelection(i);
                    break;
                }
            }
        }
    }

    private void show(Car car) {
        if (car == null) {
            finish();
            return;
        }
        List<String> manufacturers = new ArrayList<>(CarDbHelper.CATALOG.keySet());
        manufacturerSpinner.setSelection(manufacturers.indexOf(car.manufacturer));
        fillModels(car.model);
        yearText.setText(String.valueOf(car.year));
        colorText.setText(car.color);
        engineText.setText(car.engine);
        priceText.setText(String.valueOf(car.price));
    }

    /** Проверяет поля и записывает автомобиль в базу: новая строка или обновление по id. */
    private void save() {
        String color = colorText.getText().toString().trim();
        String engine = engineText.getText().toString().trim();
        int year;
        int price;
        try {
            year = Integer.parseInt(yearText.getText().toString().trim());
            price = Integer.parseInt(priceText.getText().toString().trim());
        } catch (NumberFormatException ex) {
            Toast.makeText(this, "Год и цена должны быть числами", Toast.LENGTH_SHORT).show();
            return;
        }
        if (color.isEmpty() || engine.isEmpty()) {
            Toast.makeText(this, "Заполните цвет и двигатель", Toast.LENGTH_SHORT).show();
            return;
        }
        Car car = new Car(
                carId,
                manufacturerSpinner.getSelectedItem().toString(),
                modelSpinner.getSelectedItem().toString(),
                year,
                color,
                engine,
                price);
        if (carId > 0) {
            database.update(car);
        } else {
            database.insert(car);
        }
        finish();
    }
}
