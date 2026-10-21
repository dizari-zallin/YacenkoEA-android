package com.yacenkoea.pr14;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Spinner;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.List;

/** Главный экран: список автомобилей, фильтры, сортировка по цене и переход к форме. */
public class MainActivity extends AppCompatActivity {
    static final String EXTRA_ID = "car_id";
    private static final String ALL = "Все";

    private CarDbHelper database;
    private Spinner manufacturerSpinner;
    private Spinner modelSpinner;
    private Button sortButton;
    private ListView listView;
    private boolean priceAscending = true;
    private boolean fillingSpinners;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        database = new CarDbHelper(this);
        manufacturerSpinner = findViewById(R.id.manufacturerSpinner);
        modelSpinner = findViewById(R.id.modelSpinner);
        sortButton = findViewById(R.id.sortButton);
        listView = findViewById(R.id.listView);

        fillManufacturers();
        manufacturerSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                fillModels();
                reload();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });
        modelSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if (!fillingSpinners) {
                    reload();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });
        sortButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                priceAscending = !priceAscending;
                sortButton.setText(priceAscending ? "По цене ↑" : "По цене ↓");
                reload();
            }
        });
        findViewById(R.id.addButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, CarActivity.class));
            }
        });
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Car car = (Car) parent.getItemAtPosition(position);
                Intent intent = new Intent(MainActivity.this, CarActivity.class);
                intent.putExtra(EXTRA_ID, car.id);
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        reload();
    }

    /** Список производителей плюс пункт «Все», который снимает фильтр. */
    private void fillManufacturers() {
        List<String> names = new ArrayList<>();
        names.add(ALL);
        names.addAll(CarDbHelper.CATALOG.keySet());
        manufacturerSpinner.setAdapter(new ArrayAdapter<>(
                this, android.R.layout.simple_spinner_dropdown_item, names));
    }

    /** Марки выбранного производителя. Для «Все» показаны марки всех трёх производителей. */
    private void fillModels() {
        fillingSpinners = true;
        String manufacturer = selected(manufacturerSpinner);
        List<String> names = new ArrayList<>();
        names.add(ALL);
        if (manufacturer == null || manufacturer.isEmpty()) {
            for (String[] models : CarDbHelper.CATALOG.values()) {
                for (String model : models) {
                    if (!names.contains(model)) {
                        names.add(model);
                    }
                }
            }
        } else {
            for (String model : CarDbHelper.CATALOG.get(manufacturer)) {
                names.add(model);
            }
        }
        modelSpinner.setAdapter(new ArrayAdapter<>(
                this, android.R.layout.simple_spinner_dropdown_item, names));
        fillingSpinners = false;
    }

    private void reload() {
        List<Car> cars = database.query(selected(manufacturerSpinner), selected(modelSpinner), priceAscending);
        listView.setAdapter(new CarAdapter(this, cars));
    }

    /** Пустая строка, если выбран пункт «Все». */
    private String selected(Spinner spinner) {
        Object item = spinner.getSelectedItem();
        if (item == null || ALL.equals(item.toString())) {
            return "";
        }
        return item.toString();
    }
}
