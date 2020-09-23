package com.example.trainnoti2;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

import androidx.fragment.app.Fragment;

public class SettingFragment extends Fragment {

    LinearLayout my_info;
    LinearLayout version;
    LinearLayout notification;
    LinearLayout notification_test;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_setting, container, false);

        my_info = view.findViewById(R.id.setting_myInfo);
        version = view.findViewById(R.id.setting_versionInfo);
        notification = view.findViewById(R.id.setting_notification);
        notification_test = view.findViewById(R.id.setting_notification_test);

        my_info.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), UserInfoActivity.class);
                startActivity(intent);
            }
        });
        version.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {

            }
        });
        notification.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), NotiSettingActivity.class);
                startActivity(intent);
            }
        });
        notification_test.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), AlertActivity.class);
                startActivity(intent);
            }
        });

        return view;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.e("Life-SettingFragment", "[onCreate]");
    }

    @Override
    public void onStart() {
        super.onStart();
        Log.e("Life-SettingFragment", "[onStart]");
    }

    @Override
    public void onResume() {
        super.onResume();
        Log.e("Life-SettingFragment", "[onResume]");
    }

    @Override
    public void onPause() {
        super.onPause();
        Log.e("Life-SettingFragment", "[onPause]");
    }

    @Override
    public void onStop() {
        super.onStop();
        Log.e("Life-SettingFragment", "[onStop]");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.e("Life-SettingFragment", "[onDestroy]");
    }
}
