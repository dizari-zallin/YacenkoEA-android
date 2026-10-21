package com.yacenkoea.pr14;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Локальная база каталога. При первом запуске записывает 12 автомобилей
 * трёх производителей: у Toyota и BMW по две марки, у Lada одна марка.
 */
public class CarDbHelper extends SQLiteOpenHelper {
    private static final String DB_NAME = "cars.db";
    private static final int DB_VERSION = 1;
    static final String TABLE = "cars";

    /** Допустимые марки по производителям. Новый автомобиль выбирается только из этого набора. */
    static final Map<String, String[]> CATALOG = new LinkedHashMap<>();

    static {
        CATALOG.put("Toyota", new String[]{"Camry", "Corolla"});
        CATALOG.put("BMW", new String[]{"X5", "320i"});
        CATALOG.put("Lada", new String[]{"Vesta"});
    }

    public CarDbHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE " + TABLE + " ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "manufacturer TEXT NOT NULL,"
                + "model TEXT NOT NULL,"
                + "year INTEGER NOT NULL,"
                + "color TEXT NOT NULL,"
                + "engine TEXT NOT NULL,"
                + "price INTEGER NOT NULL)");
        insertSeed(db, "Toyota", "Camry", 2022, "белый", "2.5", 2850000);
        insertSeed(db, "Toyota", "Camry", 2020, "чёрный", "2.5", 2400000);
        insertSeed(db, "Toyota", "Corolla", 2023, "серый", "1.6", 2100000);
        insertSeed(db, "Toyota", "Corolla", 2021, "синий", "1.8", 1850000);
        insertSeed(db, "BMW", "X5", 2023, "чёрный", "3.0", 8900000);
        insertSeed(db, "BMW", "X5", 2021, "белый", "3.0", 7200000);
        insertSeed(db, "BMW", "320i", 2022, "синий", "2.0", 4600000);
        insertSeed(db, "BMW", "320i", 2019, "серый", "2.0", 3100000);
        insertSeed(db, "Lada", "Vesta", 2024, "белый", "1.6", 1450000);
        insertSeed(db, "Lada", "Vesta", 2023, "красный", "1.6", 1250000);
        insertSeed(db, "Lada", "Vesta", 2022, "серый", "1.8", 1100000);
        insertSeed(db, "Lada", "Vesta", 2021, "чёрный", "1.6", 980000);
    }

    private void insertSeed(SQLiteDatabase db, String manufacturer, String model,
                            int year, String color, String engine, int price) {
        ContentValues values = new ContentValues();
        values.put("manufacturer", manufacturer);
        values.put("model", model);
        values.put("year", year);
        values.put("color", color);
        values.put("engine", engine);
        values.put("price", price);
        db.insert(TABLE, null, values);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE);
        onCreate(db);
    }

    /** Список с учётом фильтра и порядка цен. Пустой фильтр означает «все». */
    public List<Car> query(String manufacturer, String model, boolean priceAscending) {
        List<String> clauses = new ArrayList<>();
        List<String> args = new ArrayList<>();
        if (manufacturer != null && !manufacturer.isEmpty()) {
            clauses.add("manufacturer = ?");
            args.add(manufacturer);
        }
        if (model != null && !model.isEmpty()) {
            clauses.add("model = ?");
            args.add(model);
        }
        String where = clauses.isEmpty() ? null : String.join(" AND ", clauses);
        String order = priceAscending ? "price ASC" : "price DESC";
        List<Car> result = new ArrayList<>();
        try (Cursor cursor = getReadableDatabase().query(
                TABLE, null, where, args.toArray(new String[0]), null, null, order)) {
            while (cursor.moveToNext()) {
                result.add(read(cursor));
            }
        }
        return result;
    }

    public Car find(long id) {
        try (Cursor cursor = getReadableDatabase().query(
                TABLE, null, "id = ?", new String[]{String.valueOf(id)}, null, null, null)) {
            if (cursor.moveToFirst()) {
                return read(cursor);
            }
        }
        return null;
    }

    public long insert(Car car) {
        return getWritableDatabase().insert(TABLE, null, valuesOf(car));
    }

    public void update(Car car) {
        getWritableDatabase().update(TABLE, valuesOf(car), "id = ?", new String[]{String.valueOf(car.id)});
    }

    private ContentValues valuesOf(Car car) {
        ContentValues values = new ContentValues();
        values.put("manufacturer", car.manufacturer);
        values.put("model", car.model);
        values.put("year", car.year);
        values.put("color", car.color);
        values.put("engine", car.engine);
        values.put("price", car.price);
        return values;
    }

    private Car read(Cursor cursor) {
        return new Car(
                cursor.getLong(cursor.getColumnIndexOrThrow("id")),
                cursor.getString(cursor.getColumnIndexOrThrow("manufacturer")),
                cursor.getString(cursor.getColumnIndexOrThrow("model")),
                cursor.getInt(cursor.getColumnIndexOrThrow("year")),
                cursor.getString(cursor.getColumnIndexOrThrow("color")),
                cursor.getString(cursor.getColumnIndexOrThrow("engine")),
                cursor.getInt(cursor.getColumnIndexOrThrow("price")));
    }
}
