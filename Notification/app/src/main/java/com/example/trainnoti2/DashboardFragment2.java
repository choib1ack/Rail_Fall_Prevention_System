package com.example.trainnoti2;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.Toast;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseException;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class DashboardFragment2 extends Fragment {

    private RecyclerView recyclerView;
    RecyclerView.LayoutManager layoutManager;
    RecyclerView.Adapter adapter;
    ArrayList<DangerDTO> dangerData = new ArrayList<DangerDTO>();
    LinearLayout loading_circle;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_dashboard, container, false);

        loading_circle = view.findViewById(R.id.dashboard_loading);
        loading_circle.setVisibility(View.VISIBLE);

        // recycler view setting
        recyclerView = view.findViewById(R.id.dash_recyclerview);
        recyclerView.setHasFixedSize(true);
        layoutManager = new LinearLayoutManager(requireActivity());
        recyclerView.setLayoutManager(layoutManager);


        adapter = new DashboardAdapter2(requireActivity(), dangerData);
        recyclerView.setAdapter(adapter);

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = database.getReference();

//        Date now = new Date();
//        SimpleDateFormat dateFormat1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
//        DangerDTO dangerDTO = new DangerDTO("a0001", dateFormat1.format(now), "서울역 1번게이트", "미처리", "asdf1234");
//        databaseReference.child("DangerList").push().setValue(dangerDTO);


        databaseReference = database.getReference("DangerList");
        databaseReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

                if(dataSnapshot.getChildrenCount() == 0){ // 데이터가 없는 경우 로딩중 주지
                    loading_circle.setVisibility(View.GONE);
                }
                try {
                    dangerData.clear();
                    for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                        DangerDTO value = snapshot.getValue(DangerDTO.class);
                        dangerData.add(value);
                        recyclerView.scrollToPosition(dangerData.size() - 1);
                    }
                    adapter.notifyDataSetChanged();
                }catch(DatabaseException e){
                    Log.e("DB Listener trycatch", e.toString());
                }
            }
            @Override
            public void onCancelled(DatabaseError error) {
                Log.d("Firebase DB Error ", error.toString());
            }
        });
        return view;
    }



}
