package com.example.trainnoti2;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class AlertActivity extends AppCompatActivity {

    private EditText server_ip;
    private Button startServiceBtn;
    private Button endServiceBtn;


    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_alert);

        startServiceBtn = findViewById(R.id.alert_startService);
        endServiceBtn = findViewById(R.id.alert_endService2);
        server_ip = findViewById(R.id.server_ip);

        startServiceBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), NotiService.class);
                Toast.makeText(getApplicationContext(), "서비스 시작 버튼 클릭", Toast.LENGTH_SHORT).show();
                intent.putExtra("server_ip", server_ip.getText().toString());
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
    }
}