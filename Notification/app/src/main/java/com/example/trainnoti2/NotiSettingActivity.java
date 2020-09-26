package com.example.trainnoti2;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.Switch;

public class NotiSettingActivity extends AppCompatActivity {
    Switch msg_switch;
    Switch sound_switch;
    Switch vibrate_switch;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_noti_setting);

        Toolbar mToolbar = (Toolbar) findViewById(R.id.noti_toolbar);
        setSupportActionBar(mToolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        msg_switch = findViewById(R.id.noti_msg_switch);
        sound_switch = findViewById(R.id.noti_sound_switch);
        vibrate_switch = findViewById(R.id.noti_vibrate_switch);

        SharedPreferences pref = getSharedPreferences("Notification Setting File", MODE_PRIVATE);

        //해당값 불러오는 것, 해당값이 없을 경우 true호출
        msg_switch.setChecked(pref.getBoolean("msg_checked",true));
        msg_switch.setEnabled(pref.getBoolean("msg_enabled",true));
        sound_switch.setChecked(pref.getBoolean("sound_checked",true));
        sound_switch.setEnabled(pref.getBoolean("sound_enabled",true));
        vibrate_switch.setChecked(pref.getBoolean("vibrate_checked",true));
        vibrate_switch.setEnabled(pref.getBoolean("vibrate_enabled",true));


        msg_switch.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                if(msg_switch.isChecked() == true){
                    sound_switch.setEnabled(true);
                    vibrate_switch.setEnabled(true);
                }else{
                    sound_switch.setEnabled(false);
                    vibrate_switch.setEnabled(false);
                }
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case android.R.id.home:{ // 뒤로가기
                finish();
                return true;
            }
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onStop() {
        super.onStop();

        // sharedpreference 에 알림 설정 정보 저장
        SharedPreferences pref = getSharedPreferences("Notification Setting File", Activity.MODE_PRIVATE);
        SharedPreferences.Editor editor = pref.edit();
        editor.putBoolean("msg_checked", msg_switch.isChecked());
        editor.putBoolean("msg_enabled", msg_switch.isEnabled());
        editor.putBoolean("sound_checked", sound_switch.isChecked());
        editor.putBoolean("sound_enabled", sound_switch.isEnabled());
        editor.putBoolean("vibrate_checked", vibrate_switch.isChecked());
        editor.putBoolean("vibrate_enabled", vibrate_switch.isEnabled());
        editor.commit(); // SharedPreferences 데이터 저장 완료


    }}