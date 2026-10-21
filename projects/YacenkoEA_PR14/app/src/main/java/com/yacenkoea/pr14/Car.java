package com.yacenkoea.pr14;

/** Одна запись каталога: автомобиль и его характеристики. */
public class Car {
    public long id;
    public String manufacturer;
    public String model;
    public int year;
    public String color;
    public String engine;
    public int price;

    public Car(long id, String manufacturer, String model, int year,
               String color, String engine, int price) {
        this.id = id;
        this.manufacturer = manufacturer;
        this.model = model;
        this.year = year;
        this.color = color;
        this.engine = engine;
        this.price = price;
    }

    /** Первая строка списка: производитель, марка и год. */
    public String title() {
        return manufacturer + " " + model + ", " + year;
    }

    /** Вторая строка списка: цвет, объём двигателя и цена. */
    public String details() {
        return color + ", " + engine + " л, " + formatPrice(price) + " \u20BD";
    }

    static String formatPrice(int value) {
        String digits = String.valueOf(value);
        StringBuilder builder = new StringBuilder();
        int count = 0;
        for (int i = digits.length() - 1; i >= 0; i--) {
            if (count > 0 && count % 3 == 0) {
                builder.append(' ');
            }
            builder.append(digits.charAt(i));
            count++;
        }
        return builder.reverse().toString();
    }
}
