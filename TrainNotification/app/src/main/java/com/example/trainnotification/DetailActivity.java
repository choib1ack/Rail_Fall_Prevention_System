package com.example.trainnotification;

import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.content.ContextCompat;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseException;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

public class DetailActivity extends AppCompatActivity {

    TextView datetime;
    TextView location;
    Button status;
    ImageView image;
    String image_file_name;
    Button change_status_btn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        // link with xml
        datetime = findViewById(R.id.detail_datetime);
        location = findViewById(R.id.detail_location);
        status = findViewById(R.id.detail_status);
        image = findViewById(R.id.detail_image);
        change_status_btn= findViewById(R.id.detail_change_status);

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
            change_status_btn.setVisibility(View.GONE);
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

        change_status_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                makeStatusAlertDialog();
            }
        });

    }
    private void makeStatusAlertDialog(){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);

        builder.setTitle("처리 상태 변경").setMessage("정말로 변경하시겠습니까?");

        builder.setPositiveButton("네", new DialogInterface.OnClickListener(){
            @Override
            public void onClick(DialogInterface dialog, int id)
            {
//                        Toast.makeText(getApplicationContext(), "OK Click", Toast.LENGTH_SHORT).show();
                changeStatus(location.getText().toString(), datetime.getText().toString());
            }
        });

        builder.setNegativeButton("아니오", new DialogInterface.OnClickListener(){
            @Override
            public void onClick(DialogInterface dialog, int id)
            {
//                        Toast.makeText(getApplicationContext(), "Cancel Click", Toast.LENGTH_SHORT).show();
            }
        });

        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }

    private void changeStatus(final String location, final String datetime){
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        final DatabaseReference databaseReference;
        databaseReference = database.getReference("DangerList");
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                try {
                    for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                        if(snapshot.getKey().equals(location)) {
                            for(DataSnapshot dangerSnapshot : snapshot.getChildren()) {
                                DangerDTO value = dangerSnapshot.getValue(DangerDTO.class);
                                if (value.getDatetime().equals(datetime)) {
//                                    Log.e("Detail 2-->", value.toString());
                                    value.setState("처리완료");
                                    databaseReference.child(location).child(dangerSnapshot.getKey()).setValue(value);
                                    changeStateButton();
                                    break;
                                }
                            }
                            break;
                        }
                    }
                } catch (DatabaseException e) {
                    Log.e("DB Listener trycatch2", e.toString());
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {
                Log.d("Firebase DB Error ", error.toString());
            }
        });
    }
    private void changeStateButton(){
        status.setText("처리 완료");
        status.setBackground(ContextCompat.getDrawable(this, R.drawable.button_state_ok));
        change_status_btn.setVisibility(View.GONE);
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