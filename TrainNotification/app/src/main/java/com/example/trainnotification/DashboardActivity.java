package com.example.trainnotification;//package com.example.trainnoti2;
//
//import androidx.appcompat.app.AppCompatActivity;
//import androidx.recyclerview.widget.LinearLayoutManager;
//import androidx.recyclerview.widget.RecyclerView;
//
//import android.os.Bundle;
//import android.util.Log;
//import com.google.firebase.database.DataSnapshot;
//import com.google.firebase.database.DatabaseError;
//import com.google.firebase.database.DatabaseReference;
//import com.google.firebase.database.FirebaseDatabase;
//import com.google.firebase.database.ValueEventListener;
//
//import java.text.SimpleDateFormat;
//import java.util.ArrayList;
//import java.util.Date;
//
//public class DashboardActivity extends AppCompatActivity {
//
//    private RecyclerView recyclerView;
//    RecyclerView.LayoutManager layoutManager;
//    RecyclerView.Adapter adapter;
//    ArrayList<DangerDTO> dangerData = new ArrayList<DangerDTO>();
//
//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.fragment_dashboard);
//
//        // recycler view setting
//        recyclerView = findViewById(R.id.dash_recyclerview);
//        recyclerView.setHasFixedSize(true);
//        layoutManager = new LinearLayoutManager(this);
//        recyclerView.setLayoutManager(layoutManager);
//
//        adapter = new DashboardAdapter(this, dangerData);
//        recyclerView.setAdapter(adapter);
//
//        FirebaseDatabase database = FirebaseDatabase.getInstance();
//        DatabaseReference databaseReference = database.getReference();
//
//        Date now = new Date();
//        SimpleDateFormat dateFormat1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
//
////        DangerDTO dangerDTO = new DangerDTO("a0001", dateFormat1.format(now), "서울역 1번게이트", "미처리", "asdf1234");
////        databaseReference.child("DangerList").push().setValue(dangerDTO);
//
//
//        databaseReference = database.getReference("DangerList");
//        databaseReference.addValueEventListener(new ValueEventListener() {
//            @Override
//            public void onDataChange(DataSnapshot dataSnapshot) {
//                dangerData.clear();
//                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
//                    DangerDTO value = snapshot.getValue(DangerDTO.class);
//                    dangerData.add(value);
//                    Log.e("Firebase DB Value ", value.toString());
//                }
////                DangerDTO value = dataSnapshot.getValue(DangerDTO.class);
////                dangerData.add(value);
////                Log.e("Firebase DB Value ", value.toString());
//                adapter.notifyDataSetChanged();
//                Log.e("Firebase DB Result ", dangerData.toString());
//            }
//            @Override
//            public void onCancelled(DatabaseError error) {
//                Log.d("Firebase DB Error ", error.toString());
//            }
//        });
//
//    }
//}