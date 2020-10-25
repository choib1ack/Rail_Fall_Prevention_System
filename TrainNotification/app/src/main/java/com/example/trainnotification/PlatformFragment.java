package com.example.trainnotification;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

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

public class PlatformFragment extends Fragment {
    RecyclerView recyclerView;
    RecyclerView.LayoutManager layoutManager;
//    ArrayList<PlatformDTO> platformListofDB = new ArrayList<>();
    ArrayList<String> platform_name_list = new ArrayList<>();
    PlatformAdapter adapter;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_platform, container, false);
        adapter = new PlatformAdapter(requireActivity(), platform_name_list);
        recyclerView = view.findViewById(R.id.platform_recyclerview);
        recyclerView.setAdapter(adapter);
        recyclerView.setHasFixedSize(true);
        layoutManager = new LinearLayoutManager(requireActivity());
        recyclerView.setLayoutManager(layoutManager);

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = database.getReference("DangerList");

        databaseReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

//                if(dataSnapshot.getChildrenCount() == 0){ // 데이터가 없는 경우 로딩중 주지
//                    loading_circle.setVisibility(View.GONE);
//                }
                try {
                    platform_name_list.clear();
                    for (DataSnapshot platformSnapshot : dataSnapshot.getChildren()) {
                        String platform = platformSnapshot.getKey();
                        platform_name_list.add(platform);
                    }
                    adapter.notifyDataSetChanged();
//                    makePlatformNameList();

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
//    public void makePlatformNameList(){
//
//        for(int i=0; i<platformListofDB.size(); i++){
//            platform_name_list.add(platformListofDB.get(i).getPlatform_name());
//        }
//        adapter.notifyDataSetChanged();
//    }


}
