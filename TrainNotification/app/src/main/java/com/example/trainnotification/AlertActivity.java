package com.example.trainnotification;

import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

public class AlertActivity extends AppCompatActivity {

    private EditText server_ip;
    private Button startServiceBtn;
    private Button endServiceBtn;
    private Button isConnectServiceBtn;
    private TextView inConnectText;

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_alert);

        startServiceBtn = findViewById(R.id.alert_startService);
        endServiceBtn = findViewById(R.id.alert_endService2);
        isConnectServiceBtn = findViewById(R.id.alert_isConnectButton);
        server_ip = findViewById(R.id.server_ip);
        inConnectText = findViewById(R.id.alert_isConnectText);

        boolean result = isMyServiceRunning(NotiService.class);
        if(result){
            inConnectText.setText("서비스 실행중");
        }else{
            inConnectText.setText("서비스 안 실행중");
        }

        SharedPreferences pref = getSharedPreferences("Service socket info", MODE_PRIVATE);

        String stored_server_ip = pref.getString("server_ip", null);
        Log.d("AlertActivity", "server ip --->" + server_ip);
        if (stored_server_ip != null) {
            server_ip.setText(stored_server_ip);
        }

        startServiceBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), NotiService.class);
                Toast.makeText(getApplicationContext(), "서비스 시작 버튼 클릭", Toast.LENGTH_SHORT).show();
                intent.putExtra("server_ip", server_ip.getText().toString());

                // sharedpreference에도 저장.
                SharedPreferences pref = getSharedPreferences("Service socket info", MODE_PRIVATE);
                SharedPreferences.Editor editor = pref.edit();
                editor.putString("server_ip", server_ip.getText().toString());
                editor.commit();

                startService(intent);
                Toast.makeText(getApplicationContext(), "server_ip : " + server_ip.getText(), Toast.LENGTH_SHORT).show();
            }
        });
        endServiceBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), NotiService.class);
                stopService(intent);
                Toast.makeText(getApplicationContext(), "서비스 중지 버튼 클릭", Toast.LENGTH_SHORT).show();
            }
        });

        isConnectServiceBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean result = isMyServiceRunning(NotiService.class);
                if(result){
                    Toast.makeText(getApplicationContext(), "서비스 실행중", Toast.LENGTH_SHORT).show();
                    inConnectText.setText("서비스 실행중");
                }else{
                    Toast.makeText(getApplicationContext(), "서비스 안 실행중", Toast.LENGTH_SHORT).show();
                    inConnectText.setText("서비스 안 실행중");
                }
            }
        });

//        isConnectServiceBtn.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                NotiService test = new NotiService();
//                test.createNotification("테스트 위치", "테스트데이트타임", "테스트이미지", "테스트이미지이름");
//                String location, String datetime, Bitmap bm, String image_name
//            }
//        });

    }

    private boolean isMyServiceRunning(Class<?> serviceClass) {
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (serviceClass.getName().equals(service.service.getClassName())) {
                return true;
            }
        }
        return false;
    }
}