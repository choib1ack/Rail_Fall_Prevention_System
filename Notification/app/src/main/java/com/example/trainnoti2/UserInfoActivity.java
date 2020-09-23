package com.example.trainnoti2;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;

public class UserInfoActivity extends AppCompatActivity {

    Button logout_btn;
    TextView user_name;
    TextView email;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_info);

        Toolbar mToolbar = (Toolbar) findViewById(R.id.user_info_toolbar);
        setSupportActionBar(mToolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        final FirebaseAuth auth = FirebaseAuth.getInstance();
//        Log.e("userinfo", auth.getCurrentUser().getDisplayName()+"/"+auth.getCurrentUser().getEmail()+"/"+auth.getCurrentUser().getPhoneNumber());

        logout_btn = findViewById(R.id.info_logout_button);
        user_name = findViewById(R.id.info_name);
        email = findViewById(R.id.info_email);

        user_name.setText(auth.getCurrentUser().getDisplayName());
        email.setText(auth.getCurrentUser().getEmail());

        logout_btn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                auth.signOut();

                finishAffinity();
                Intent intent = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(intent);
//                System.exit(0);
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
}