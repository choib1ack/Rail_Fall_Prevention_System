package com.example.Notification;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.content.ContextCompat;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

public class DetailActivity extends AppCompatActivity {

    TextView datetime;
    TextView location;
    Button status;
    ImageView image;
    String image_file_name;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        // link with xml
        datetime = findViewById(R.id.detail_datetime);
        location = findViewById(R.id.detail_location);
        status = findViewById(R.id.detail_status);
        image = findViewById(R.id.detail_image);

        Toolbar mToolbar = findViewById(R.id.detail_toolbar);
        setSupportActionBar(mToolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        final LinearLayout loading_circle = findViewById(R.id.detail_loading);
        loading_circle.setVisibility(View.VISIBLE);
        // get intent data
        Intent intent = getIntent();
        datetime.setText(intent.getStringExtra("datetime"));
        location.setText(intent.getStringExtra("location"));
        if(intent.getStringExtra("status").equals("미처리")){
            status.setText(intent.getStringExtra("status"));
            status.setBackground(ContextCompat.getDrawable(this, R.drawable.button_state_no));
        }else{
            status.setText(intent.getStringExtra("status"));
            status.setBackground(ContextCompat.getDrawable(this, R.drawable.button_state_ok));
        }
        image_file_name = intent.getStringExtra("image_name");
//        image.setImageBitmap(intent.get("status"));

        FirebaseStorage storage = FirebaseStorage.getInstance();
        StorageReference storageRef = storage.getReference();
        StorageReference pathReference = storageRef.child(image_file_name);

        pathReference.getDownloadUrl().addOnCompleteListener(new OnCompleteListener<Uri>() {
            @Override
            public void onComplete(@NonNull Task<Uri> task) {
                if (task.isSuccessful()) {
                    Glide.with(getApplicationContext())
                            .load(task.getResult())
                            .into(image);
                    loading_circle.setVisibility(View.GONE);
                } else {
                    Toast.makeText(getApplicationContext(), task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                    loading_circle.setVisibility(View.GONE);
                }
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch(item.getItemId()) {
            case android.R.id.home:
                return true;
        }
        return super.onOptionsItemSelected(item);
    }
}