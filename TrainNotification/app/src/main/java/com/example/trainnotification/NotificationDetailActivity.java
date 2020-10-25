package com.example.trainnotification;

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
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.app.NotificationManagerCompat;
import androidx.core.content.ContextCompat;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseException;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

public class NotificationDetailActivity extends AppCompatActivity {

    TextView datetime;
    TextView location;
    Button status;
    ImageView image;
    String image_file_name;
    LinearLayout loading_circle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification_detail);
        Log.e("NotificationDetail", "onCreate");
        NotificationManagerCompat.from(this).cancel(1);
        // link with xml
        datetime = findViewById(R.id.notification_detail_datetime);
        location = findViewById(R.id.notification_detail_location);
        status = findViewById(R.id.notification_detail_status);
        image = findViewById(R.id.notification_detail_image);

        Toolbar mToolbar = findViewById(R.id.notification_detail_toolbar);
        setSupportActionBar(mToolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        loading_circle = findViewById(R.id.notification_detail_loading);
        loading_circle.setVisibility(View.VISIBLE);
        // get intent data
        Intent intent = getIntent();
        String noti_datetime = intent.getStringExtra("datetime");
        String noti_location = intent.getStringExtra("location");

        findNotificationDataInDB(noti_datetime, noti_location);


    }

    public void findNotificationDataInDB(final String datetime, final String location) {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference;
        Log.e("Detail 0-->", datetime);
        final DangerDTO[] result = {new DangerDTO()};

        databaseReference = database.getReference("DangerList");
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

                if (dataSnapshot.getChildrenCount() == 0) { // 데이터가 없는 경우 로딩중 주지
                    loading_circle.setVisibility(View.GONE);
                }
                try {
                    for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                        DangerDTO value = snapshot.getValue(DangerDTO.class);
                        Log.e("Detail 1-->", value.getDatetime());
//                        assert value != null;
//                        if (value.getDatetime().equals(datetime) && value.getLocation().equals(location)) {
                        if (value.getDatetime().equals(datetime)) {
                            Log.e("Detail 2-->", value.toString());
                            result[0] = value;
                            setUI(result[0]);
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

    public void setUI(final DangerDTO data) {
        datetime.setText(data.getDatetime());
        location.setText(data.getLocation());
        if (data.getState().equals("미처리")) {
            status.setText("미처리");
            status.setBackground(ContextCompat.getDrawable(this, R.drawable.button_state_no));
        } else {
            status.setText("처리완료");
            status.setBackground(ContextCompat.getDrawable(this, R.drawable.button_state_ok));
        }
        image_file_name = data.getImage_name();

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
                    checkRead(data);
                } else {
                    Toast.makeText(getApplicationContext(), task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                    loading_circle.setVisibility(View.GONE);
                }
            }
        });
    }

    public void checkRead(DangerDTO data) {
        // 해당 알림 객체 찾아서 read=true로 변경
        final String datetime = data.getDatetime();
        final String location = data.getLocation();

        final String myUID = FirebaseAuth.getInstance().getUid();

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        final DatabaseReference databaseReference;

        databaseReference = database.getReference("Notification");
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

                try {
                    for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                        if (snapshot.getKey().equals(myUID)) {
                            for (DataSnapshot my_noti_snapshot : snapshot.getChildren()) {
                                NotiDTO value = my_noti_snapshot.getValue(NotiDTO.class);
//                                if (value.getDatetime().equals(datetime) && value.getLocation().equals(location)) {
                                if (value.getDatetime().equals(datetime)) {
                                    value.setChecked(true);
                                    databaseReference.child(myUID).child(my_noti_snapshot.getKey()).setValue(value);
                                    break;
                                }
                            }
                            break;
                        }
                    }
                } catch (DatabaseException e) {
                    Log.e("DB Listener trycatch1", e.toString());
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {
                Log.d("Firebase DB Error ", error.toString());
            }
        });

    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                return true;
        }
        return super.onOptionsItemSelected(item);
    }
}