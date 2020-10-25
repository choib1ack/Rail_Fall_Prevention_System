package com.example.trainnotification;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class PlatformDetailActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    RecyclerView.LayoutManager layoutManager;
    PlatformDetailAdapter adapter;
    ArrayList<DangerDTO> dangerDataOfPlatform = new ArrayList<DangerDTO>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_platform_detail);

        Intent intent = getIntent();
        String platform_name = intent.getStringExtra("platform_name");

        // recycler view setting
        recyclerView = findViewById(R.id.platform_detail_recyclerview);
        recyclerView.setHasFixedSize(true);
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);

        adapter = new PlatformDetailAdapter(this, dangerDataOfPlatform);
        recyclerView.setAdapter(adapter);

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = database.getReference();

//        Date now = new Date();
//        SimpleDateFormat dateFormat1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

//        DangerDTO dangerDTO = new DangerDTO("a0001", dateFormat1.format(now), "서울역 1번게이트", "미처리", "asdf1234");
//        databaseReference.child("DangerList").push().setValue(dangerDTO);


        databaseReference = database.getReference("DangerList").child(platform_name);
        databaseReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                dangerDataOfPlatform.clear();
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    DangerDTO value = snapshot.getValue(DangerDTO.class);
                    dangerDataOfPlatform.add(value);
                }
                adapter.notifyDataSetChanged();
            }
            @Override
            public void onCancelled(DatabaseError error) {
                Log.d("Firebase DB Error ", error.toString());
            }
        });


    }



}