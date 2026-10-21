package com.yacenkoea.pr14;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import java.util.List;

/** Рисует одну строку списка: название автомобиля и его характеристики. */
public class CarAdapter extends ArrayAdapter<Car> {
    public CarAdapter(Context context, List<Car> cars) {
        super(context, 0, cars);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_car, parent, false);
        }
        Car car = getItem(position);
        TextView title = convertView.findViewById(R.id.carTitle);
        TextView details = convertView.findViewById(R.id.carDetails);
        if (car != null) {
            title.setText(car.title());
            details.setText(car.details());
        }
        return convertView;
    }
}
