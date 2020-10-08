//package com.example.trainnoti2;
//
//import android.os.Bundle;
//import android.util.Log;
//import android.view.LayoutInflater;
//import android.view.View;
//import android.view.ViewGroup;
//import android.widget.LinearLayout;
//
//import androidx.fragment.app.Fragment;
//import androidx.recyclerview.widget.LinearLayoutManager;
//import androidx.recyclerview.widget.RecyclerView;
//import com.google.firebase.database.DataSnapshot;
//import com.google.firebase.database.DatabaseError;
//import com.google.firebase.database.DatabaseReference;
//import com.google.firebase.database.FirebaseDatabase;
//import com.google.firebase.database.ValueEventListener;
//import java.text.SimpleDateFormat;
//import java.util.ArrayList;
//import java.util.Date;
//
//public class DashboardFragment extends Fragment {
//
//    private RecyclerView recyclerView;
//    RecyclerView.LayoutManager layoutManager;
//    RecyclerView.Adapter adapter;
//    ArrayList<DangerDTO> dangerData = new ArrayList<DangerDTO>();
//
//
//    @Override
//    public View onCreateView(LayoutInflater inflater, ViewGroup container,
//                             Bundle savedInstanceState) {
//        View view = inflater.inflate(R.layout.fragment_dashboard, container, false);
//
//        final LinearLayout loading_circle = view.findViewById(R.id.dashboard_loading);
//        loading_circle.setVisibility(View.VISIBLE);
//
//        // recycler view setting
//        recyclerView = view.findViewById(R.id.dash_recyclerview);
//        recyclerView.setHasFixedSize(true);
//        layoutManager = new LinearLayoutManager(requireActivity());
//        recyclerView.setLayoutManager(layoutManager);
//
//        adapter = new DashboardAdapter(requireActivity(), dangerData);
//        recyclerView.setAdapter(adapter);
//
//        FirebaseDatabase database = FirebaseDatabase.getInstance();
//        DatabaseReference databaseReference = database.getReference();
//
////        Date now = new Date();
////        SimpleDateFormat dateFormat1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
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
//                }
//                adapter.notifyDataSetChanged();
//                loading_circle.setVisibility(View.GONE);
//            }
//            @Override
//            public void onCancelled(DatabaseError error) {
//                Log.d("Firebase DB Error ", error.toString());
//            }
//        });
//
//
//        return view;
//    }
//
//
//
//}
