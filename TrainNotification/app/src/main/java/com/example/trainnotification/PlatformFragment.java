package com.example.trainnotification;

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

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseException;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

import static java.lang.Thread.sleep;

public class PlatformFragment extends Fragment {
    RecyclerView recyclerView_star;
    RecyclerView recyclerView_normal;
    RecyclerView.LayoutManager layoutManager_star;
    RecyclerView.LayoutManager layoutManager_normal;
    ArrayList<String> platform_star_name_list = new ArrayList<>();
    ArrayList<String> platform_normal_name_list = new ArrayList<>();
    PlatformAdapter adapter_normal;
    PlatformStarAdapter adapter_star;
    LinearLayout loading_circle;

    String uid = FirebaseAuth.getInstance().getUid();

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_platform, container, false);

        loading_circle = view.findViewById(R.id.platform_loading);
        loading_circle.setVisibility(View.VISIBLE);

        recyclerviewInit(view);
        getPlatformList();


        return view;
    }

    private void recyclerviewInit(View view){
        adapter_normal = new PlatformAdapter(requireActivity(), platform_normal_name_list);
        recyclerView_normal = view.findViewById(R.id.platform_recyclerview_normal);
        recyclerView_normal.setAdapter(adapter_normal);
        recyclerView_normal.setHasFixedSize(true);
        layoutManager_normal = new LinearLayoutManager(requireActivity());
        recyclerView_normal.setLayoutManager(layoutManager_normal);

        adapter_star = new PlatformStarAdapter(requireActivity(), platform_star_name_list);
        recyclerView_star = view.findViewById(R.id.platform_recyclerview_star);
        recyclerView_star.setAdapter(adapter_star);
        recyclerView_star.setHasFixedSize(true);
        layoutManager_star = new LinearLayoutManager(requireActivity());
        recyclerView_star.setLayoutManager(layoutManager_star);
    }

    private void getPlatformList(){
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = database.getReference("DangerList");

        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

//                if(dataSnapshot.getChildrenCount() == 0){ // 데이터가 없는 경우 로딩중 주지
//                    loading_circle.setVisibility(View.GONE);
//                }
                try {
                    platform_normal_name_list.clear();
                    for (DataSnapshot platformSnapshot : dataSnapshot.getChildren()) {
                        String platform = platformSnapshot.getKey();
                        platform_normal_name_list.add(platform);
                    }
//                    adapter_normal.notifyDataSetChanged();
                    findStarPlatform();

                }catch(DatabaseException e){
                    Log.e("DB Listener trycatch", e.toString());
                }
            }
            @Override
            public void onCancelled(DatabaseError error) {
                Log.d("Firebase DB Error ", error.toString());
            }
        });
    }
    private void findStarPlatform(){

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = database.getReference("MyPlatform").child(uid);
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

//                if(dataSnapshot.getChildrenCount() == 0){ // 데이터가 없는 경우 로딩중 주지
//                    loading_circle.setVisibility(View.GONE);
//                }
                try {
                    platform_star_name_list.clear();

                    if(dataSnapshot.getChildrenCount()==0){

                    }else {
                        StarPlatformDTO value = dataSnapshot.getValue(StarPlatformDTO.class);
                        ArrayList<String> star_platform_list = value.getStar_platform_list();
                        for(int i=0; i<star_platform_list.size(); i++) {
                            String tmp = star_platform_list.get(i);
                            if(platform_normal_name_list.contains(tmp)){
                                platform_normal_name_list.remove(tmp);
                                platform_star_name_list.add(tmp);
                            }
                        }
                    }

                    adapter_star.notifyDataSetChanged();
                    adapter_normal.notifyDataSetChanged();
                    loading_circle.setVisibility(View.GONE);
                }catch(DatabaseException e){
                    Log.e("DB Listener trycatch3", e.toString());
                }
            }
            @Override
            public void onCancelled(DatabaseError error) {
                Log.d("Firebase DB Error ", error.toString());
            }
        });
    }

    public void changeStarState(String platform_name){


        if(!platform_star_name_list.contains(platform_name)) {
            platform_normal_name_list.remove(platform_name);
            platform_star_name_list.add(platform_name);
            adapter_star.notifyDataSetChanged();
            adapter_normal.notifyDataSetChanged();
            Toast.makeText(requireContext(), "즐겨찾기 추가됨", Toast.LENGTH_SHORT).show();
        }else{
            platform_star_name_list.remove(platform_name);
            platform_normal_name_list.add(platform_name);
            adapter_star.notifyDataSetChanged();
            adapter_normal.notifyDataSetChanged();
            Toast.makeText(requireContext(), "즐겨찾기 취소됨", Toast.LENGTH_SHORT).show();
        }
        loading_circle.setVisibility(View.VISIBLE);
        changeStarStateOfDB();
    }
    public void changeStarStateOfDB(){
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = database.getReference("MyPlatform").child(uid);

        StarPlatformDTO data = new StarPlatformDTO(platform_star_name_list);
        databaseReference.setValue(data);
//        try
//        {
//            sleep(200);
//        } catch (InterruptedException e)
//        {
//            e.printStackTrace();
//        }
        loading_circle.setVisibility(View.GONE);
    }
}
