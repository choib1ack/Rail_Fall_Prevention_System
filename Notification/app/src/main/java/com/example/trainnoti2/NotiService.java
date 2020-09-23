package com.example.trainnoti2;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;
import android.view.inputmethod.InputMethodManager;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;

public class NotiService extends Service {
    private String channel_id = "";
    private String server_ip = "";
    String TAG = "NotiService";
    private Socket socket;
    Boolean isReceiving = true;

    public NotiService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(TAG, "서비스 시작!");
        notificationSetting();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "알람 전송");

        if(intent == null){
            return Service.START_STICKY;
        }else{
            //Connect Thread 실행
            server_ip = intent.getStringExtra("server_ip");
            Log.d(TAG, "destroyed");
            ConnectThread thread = new ConnectThread(server_ip);
            thread.start();
        }
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        Log.d(TAG, "destroyed");
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
            Log.d(TAG, "socket close 실패");
        }
        super.onDestroy();
    }

    private void notificationSetting(){
        // 알림 설정 (소리, 진동, 무음)--------------------------------------------------------------------------------
        // 알람 스위치 상태 불러오기, 저장된 상태없으면 default값은 true
        SharedPreferences pref = getSharedPreferences("Notification Setting File", MODE_PRIVATE);
        boolean sound_state = pref.getBoolean("sound_checked", true);
        boolean vibrate_state = pref.getBoolean("vibrate_checked", true);
        boolean msg_state = pref.getBoolean("msg_checked", true);

        // Default-> 진동, 소리 모두 on 상태
        channel_id= "Vibrate&Sound";

        // 스위치 상태에 따라 channel ID 선택
        // Massage 스위치 off
        if (!msg_state) {
            channel_id = "MassageDisable";
        }
        // Sound 스위치 off, Vibrate 스위치 on
        else if (!sound_state && vibrate_state) {
            channel_id = "Vibrate";
        }
        // Sound 스위치 on, Vibrate 스위치 off
        else if (sound_state && !vibrate_state) {
            channel_id = "Sound";
        }
        // Sound, Vibrate 둘다 off
        else if (!sound_state && !vibrate_state) {
            channel_id = "Silent";
        }
        // 알림 설정 끝 --------------------------------------------------------------------------------
    }


    @RequiresApi(api = Build.VERSION_CODES.M)
    @SuppressLint("WrongConstant")
    private void createNotification(String datetime, String location, Bitmap bm, String image_name) {

        // 탭을 클릭하면 click activity로 넘어감
        Intent intent = new Intent(getApplicationContext(), AlertClickActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent, 0);

        // 헤드업 알림을 위한 인텐트
        Intent fullScreenIntent = new Intent(this, AlertClickActivity.class);
        PendingIntent fullScreenPendingIntent = PendingIntent.getActivity(this, 0, fullScreenIntent, PendingIntent.FLAG_UPDATE_CURRENT);

        // 탭 버튼을 클릭하면 넘어감
        Intent skipIntent = new Intent(getApplicationContext(), AlertRemoveActivity.class);
        skipIntent.setFlags(skipIntent.FLAG_ACTIVITY_NEW_TASK);
        PendingIntent skipPending = PendingIntent.getActivity(this, 0, skipIntent, 0);

        Uri notificationSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, channel_id);

        builder.setSmallIcon(R.mipmap.ic_launcher);
        builder.setContentTitle("위험 감지 알림");
        builder.setContentText("["+location+"] "+datetime);
        builder.setColor(Color.GRAY);

        builder.setLargeIcon(bm);
        builder.setStyle(new NotificationCompat.BigPictureStyle().bigPicture(bm).bigLargeIcon(bm));

        builder.setDefaults(Notification.DEFAULT_VIBRATE); //알람이 오면 진동 울리기 (진동이 켜져있을 경우)
        builder.setSound(notificationSound);
        builder.setPriority(NotificationCompat.PRIORITY_HIGH);
        builder.setFullScreenIntent(fullScreenPendingIntent, true);

        builder.setContentIntent(pendingIntent); // 펼치기 전 인텐트
        builder.addAction(R.drawable.ic_baseline_details_24, getString(R.string.detail), pendingIntent);
        builder.addAction(R.drawable.ic_baseline_skip_next_24, getString(R.string.later), skipPending);
        builder.setAutoCancel(true); // 사용자가 탭을 클릭하면 자동 제거

        NotificationManager notificationManager = getSystemService(NotificationManager.class);

        // id값은 정의해야하는 각 알림의 고유한 int값
        notificationManager.notify(1, builder.build());

        // 받은 알림 데이터 저장
        sendNotificationDataToDB(location, datetime, image_name, false);
    }

    private void createNotificationChannel() {
        // Create the NotificationChannel, but only on API 26+ because
        // the NotificationChannel class is new and not in the support library
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            String descriptionText = "descriptionText";
            Integer importance = NotificationManager.IMPORTANCE_HIGH;

            // Vibrate & Sound Channel
            NotificationChannel vs_channel = new NotificationChannel("Vibrate&Sound", "진동+소리", importance);
            vs_channel.setDescription(descriptionText);
            // Vibrate Channel
            NotificationChannel v_channel = new NotificationChannel("Vibrate", "진동", importance);
            vs_channel.setDescription(descriptionText);
            // Sound Channel
            NotificationChannel s_channel = new NotificationChannel("Sound", "소리", importance);
            vs_channel.setDescription(descriptionText);
            // Silent Channel
            NotificationChannel channel = new NotificationChannel("Silent", "무음", importance);
            vs_channel.setDescription(descriptionText);
            // Massage disabled channel
            NotificationChannel md_channel = new NotificationChannel("MassageDisable", "메시지알림off", NotificationManager.IMPORTANCE_NONE);
            vs_channel.setDescription(descriptionText);

            // Silent Channel
            channel.setVibrationPattern(new long[]{0}); // 진동 끄기
            channel.enableVibration(true); // 진동 끄기
            channel.setSound(null,null);

            // Sound Channel
            channel.setVibrationPattern(new long[]{0}); // 진동 끄기
            s_channel.enableVibration(true); // 진동 끄기

            // Vibrate Channel
            v_channel.enableVibration(true);
            v_channel.setSound(null,null);

            // Vibrate & Sound Channel
            vs_channel.enableVibration(true);

            // Register the channel with the system
            NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(channel);
            notificationManager.createNotificationChannel(vs_channel);
            notificationManager.createNotificationChannel(v_channel);
            notificationManager.createNotificationChannel(s_channel);
            notificationManager.createNotificationChannel(md_channel);
        }
    }

    public void sendNotificationDataToDB(String datetime, String location, String image_name, Boolean isChecked){
        FirebaseAuth auth = FirebaseAuth.getInstance();
        String uid = auth.getCurrentUser().getUid();
        DatabaseReference ref = FirebaseDatabase.getInstance().getReference("Notification");

        NotiDTO dto = new NotiDTO(datetime, location, image_name, isChecked);
        ref.child(uid).push().setValue(dto);
    }

    class ConnectThread extends Thread {
        String hostname;

        public ConnectThread(String addr) {
            hostname = addr;
        }

        // byte 배열을 비트맵으로 바꾸는 함수
        public Bitmap byteToBitmap(byte[] bytedata) {
            Bitmap bitmap = BitmapFactory.decodeByteArray(bytedata, 0, bytedata.length);
            return bitmap;
        }

        public void run() {
            try { //클라이언트 소켓 생성

                int port = 9999;
                socket = new Socket(hostname, port);
                Log.d(TAG, "Socket 생성, 연결.");

//                DataReceiveThread sthread = new DataReceiveThread();
//                sthread.start();

                try {
                    Log.d(TAG, "데이터 수신 준비");

                    InputStream input = socket.getInputStream();

                    int count = 0;
                    while (isReceiving) {
                        while (input.available() <= 0) {
                        } // 이거 효율적이게 바꿔야할듯

                        int filesize;
                        byte[] tmp = new byte[2];
                        input.read(tmp, 0, tmp.length);
                        int info_data_len = Integer.parseInt(new String(tmp));

                        byte[] info_data = new byte[info_data_len];
                        input.read(info_data, 0, info_data.length);

                        String info = new String(info_data);

                        final String[] infolist = info.split("/");
                        filesize = Integer.parseInt(infolist[0]);
                        Log.d(TAG, "filesize ----> " + filesize);

                        byte[] image_data = new byte[filesize];
                        byte[] buffer = new byte[1024];
                        int img_offset = 0;
                        while (true) {
//                            Log.d(TAG, "inputstream available ----> " + input.available() + " ");
                            int bytes_read = input.read(buffer, 0, buffer.length); // 버퍼만큼 바이트 데이터 수신, 데이터는 버퍼 안에 있고, 사이즈 리턴
                            System.arraycopy(buffer, 0, image_data, img_offset, bytes_read);

                            img_offset += bytes_read;
//                            Log.d(TAG, "img_offset ----> " + img_offset + " ");
                            if (img_offset >= filesize) {
                                break;
                            }
                        }

                        // 비트맵 이미지 imageView로 설정
                        final Bitmap bm = byteToBitmap(image_data);

                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                            // 알림 생성
                            Log.e(TAG, "알림 생성!");
                            createNotification(infolist[1], infolist[2], bm, infolist[3]); // location, datetime, image name
                        }
                        Log.e(TAG, count + "번째 이미지 받기 끝!");
                        count++; // 테스트용
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.e(TAG, "데이터 수신 에러");
                }

            } catch (UnknownHostException uhe) { // 소켓 생성 시 전달되는 호스트(www.unknown-host.com)의 IP를 식별할 수 없음.

                Log.e(TAG, " 생성 Error : 호스트의 IP 주소를 식별할 수 없음.(잘못된 주소 값 또는 호스트 이름 사용)");

            } catch (IOException ioe) { // 소켓 생성 과정에서 I/O 에러 발생.
                Log.e(TAG, " 생성 Error : 네트워크 응답 없음");

            } catch (SecurityException se) { // security manager에서 허용되지 않은 기능 수행.

                Log.e(TAG, " 생성 Error : 보안(Security) 위반에 대해 보안 관리자(Security Manager)에 의해 발생. (프록시(proxy) 접속 거부, 허용되지 않은 함수 호출)");


            } catch (IllegalArgumentException le) { // 소켓 생성 시 전달되는 포트 번호(65536)이 허용 범위(0~65535)를 벗어남.
                Log.e(TAG, " 생성 Error : 메서드에 잘못된 파라미터가 전달되는 경우 발생.(0~65535 범위 밖의 포트 번호 사용, null 프록시(proxy) 전달)");
            }
        }



//        class DataReceiveThread extends Thread {
//
//            public DataReceiveThread() {}
//
//            // byte 배열을 비트맵으로 바꾸는 함수
//            public Bitmap byteToBitmap(byte[] bytedata) {
//                Bitmap bitmap = BitmapFactory.decodeByteArray(bytedata, 0, bytedata.length);
//                return bitmap;
//            }
//
//            public void run() {
//
//                try {
//                    Log.d(TAG, "데이터 수신 준비");
//
//                    InputStream input = socket.getInputStream();
//
//                    int count = 0;
//                    while (isReceiving) {
//                        while (input.available() <= 0) {
//                        } // 이거 효율적이게 바꿔야할듯
//
//                        int filesize;
//                        byte[] tmp = new byte[2];
//                        input.read(tmp, 0, tmp.length);
//                        int info_data_len = Integer.parseInt(new String(tmp));
//
//                        byte[] info_data = new byte[info_data_len];
//                        input.read(info_data, 0, info_data.length);
//
//                        String info = new String(info_data);
//
//                        final String[] infolist = info.split("/");
//                        filesize = Integer.parseInt(infolist[0]);
//                        Log.d(TAG, "filesize ----> " + filesize);
//
//                        byte[] image_data = new byte[filesize];
//                        byte[] buffer = new byte[1024];
//                        int img_offset = 0;
//                        while (true) {
////                            Log.d(TAG, "inputstream available ----> " + input.available() + " ");
//                            int bytes_read = input.read(buffer, 0, buffer.length); // 버퍼만큼 바이트 데이터 수신, 데이터는 버퍼 안에 있고, 사이즈 리턴
//                            System.arraycopy(buffer, 0, image_data, img_offset, bytes_read);
//
//                            img_offset += bytes_read;
////                            Log.d(TAG, "img_offset ----> " + img_offset + " ");
//                            if (img_offset >= filesize) {
//                                break;
//                            }
//                        }
//
//                        // 비트맵 이미지 imageView로 설정
//                        final Bitmap bm = byteToBitmap(image_data);
//
//                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
//                            // 알림 생성
//                            Log.e(TAG, "알림 생성!");
//                            createNotification(infolist[1], infolist[2], bm);
//                        }
//                        Log.e(TAG, count + "번째 이미지 받기 끝!");
//                        count++; // 테스트용
//                    }
//                } catch (IOException e) {
//                    e.printStackTrace();
//                    Log.e(TAG, "수신 에러");
//                }
//            }
//        }
    }
}
