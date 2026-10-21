package com.yacenkoea.pr8;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import java.io.IOException;
import java.io.InputStream;

/** Экран выбора картинки из галереи и смены режима масштабирования. */
public class MainActivity extends AppCompatActivity {
    static final int GALLERY_REQUEST = 1;
    ImageView imageView;
    TextView scaleLabel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
        scaleLabel = findViewById(R.id.scaleLabel);
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Запрос изображения из галереи устройства.
                Intent photoPickerIntent = new Intent(Intent.ACTION_PICK);
                photoPickerIntent.setType("image/*");
                startActivityForResult(photoPickerIntent, GALLERY_REQUEST);
            }
        });
        findViewById(R.id.btnCenter).setOnClickListener(v -> applyScale(ImageView.ScaleType.CENTER, "CENTER"));
        findViewById(R.id.btnCrop).setOnClickListener(v -> applyScale(ImageView.ScaleType.CENTER_CROP, "CENTER_CROP"));
        findViewById(R.id.btnInside).setOnClickListener(v -> applyScale(ImageView.ScaleType.CENTER_INSIDE, "CENTER_INSIDE"));
        findViewById(R.id.btnFit).setOnClickListener(v -> applyScale(ImageView.ScaleType.FIT_CENTER, "FIT_CENTER"));
        findViewById(R.id.btnFill).setOnClickListener(v -> applyScale(ImageView.ScaleType.FIT_XY, "FIT_XY"));
    }

    /** Меняет способ вписывания картинки в ImageView. */
    private void applyScale(ImageView.ScaleType type, String name) {
        imageView.setScaleType(type);
        scaleLabel.setText("Масштаб: " + name);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent) {
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent);
        if (requestCode == GALLERY_REQUEST && resultCode == RESULT_OK && imageReturnedIntent != null) {
            Uri selectedImage = imageReturnedIntent.getData();
            if (selectedImage == null) {
                return;
            }
            try (InputStream stream = getContentResolver().openInputStream(selectedImage)) {
                Bitmap bitmap = BitmapFactory.decodeStream(stream);
                imageView.setImageBitmap(bitmap);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
