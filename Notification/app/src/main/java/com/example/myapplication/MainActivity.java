package com.example.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    public TextView Toptext;
    public TextView datatext;
    public TextView byText;
    public Button StartButton;
    public Button ConnButton;
    public Button DiconButton;
    public Button IsconButton;
    public ImageView ImgView;
    private Socket socket;

    private DataOutputStream dos;
    private DataInputStream dis;

    // fixme: TAG
    String TAG = "socketTest";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        ConnButton = findViewById(R.id.button1);
        StartButton = findViewById(R.id.button2);
        DiconButton = findViewById(R.id.button4);
        IsconButton = findViewById(R.id.button5);
        ImgView = findViewById(R.id.image1);
        final EditText ipNumber = findViewById(R.id.ipText);


        Log.i(TAG, "Application createad");

        // 안드로이드 허가 권한 설정
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }


        // connect 버튼 이벤트 -> 서버에 연결 요청
        ConnButton.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getApplicationContext(), "Connect 시도", Toast.LENGTH_SHORT).show();
                String addr = ipNumber.getText().toString().trim();
                ConnectThread thread = new ConnectThread(addr);

                //키보드 자동 내리기
                InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                imm.hideSoftInputFromWindow(ipNumber.getWindowToken(), 0);

                thread.start();


            }
        });

        // start 버튼 이벤트 -> 서버로부터 이미지 수신
        StartButton.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                StartThread sthread = new StartThread();
                StartButton.setEnabled(false);
                sthread.start();
            }
        });

        // disconnect 버튼 이벤트 -> 연결 종료
        DiconButton.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    socket.close();
                    Toptext.setText("연결 종료됨");
                    Toast.makeText(getApplicationContext(), "DisConnect", Toast.LENGTH_SHORT).show();
                    DiconButton.setEnabled(false);
                    ConnButton.setEnabled(true);
                    StartButton.setEnabled(false);
                } catch (IOException e) {
                    e.printStackTrace();
                    Toast.makeText(getApplicationContext(), "DisConnect 실패", Toast.LENGTH_SHORT).show();
                }
            }
        });

        // connect확인 버튼 이벤트 -> 연결 확인
        IsconButton.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean iscon = socket.isClosed();
                InetAddress addr = socket.getInetAddress();
                String tmp = addr.getHostAddress();
                if (!iscon) {
                    Toast.makeText(getApplicationContext(), tmp + " 연결 중", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getApplicationContext(), "연결이 안 되어 있습니다.", Toast.LENGTH_SHORT).show();
                }
            }
        });

    }

    // fixme: Start 버튼 클릭 시 데이터 수신.
    class StartThread extends Thread {

        int size;


        public StartThread() {

            datatext = findViewById(R.id.recvByte);
            byText = findViewById(R.id.ByteText);
        }

        // byte 배열을 비트맵으로 바꾸는 함수
        public Bitmap byteToBitmap(byte[] bytedata) {
            Bitmap bitmap = BitmapFactory.decodeByteArray(bytedata, 0, bytedata.length);
            return bitmap;
        }

        // 스트링을 비트맵 형식으로 바꾸는 함수
        public Bitmap StringToBitMap(String encodeString) {
            try {
                byte[] encodeByte = Base64.decode(encodeString, Base64.DEFAULT);
                Bitmap bitmap = BitmapFactory.decodeByteArray(encodeByte, 0, encodeByte.length);
//                Log.d(TAG, "스트링" + encodeString);
//                Log.d(TAG, "비트맵" + bitmap);
                return bitmap;
            } catch (Exception e) {
                e.getMessage();
                return null;
            }
        }

        public void run() {

            try {

                // 커넥션을 하는 동시에 서버에서 데이터를 전송함
                // start 버튼을 누르면 전송된 데이터를 받음 (이미지 형식으로 변환)
                Log.d(TAG, "데이터 수신 준비");

//                dis = new DataInputStream(socket.getInputStream());

                byte[] image_data = null;
                // 바이트 받을 버퍼 -> 1024 바이트씩 수신
                byte[] buffer = new byte[1024];
                InputStream input = socket.getInputStream();
                
                while (true) {
                    // 버퍼만큼 바이트 데이터 수신, 데이터는 버퍼 안에 있고, 사이즈 리턴
                    int size = input.read(buffer);

                    if (size != -1) { // 그러니까 데이터가 있으면
                        byte[] tmp = buffer.clone();
                        if (image_data == null) {
                            image_data = tmp.clone();
                            Log.e(TAG, "image1 : " + image_data);
                        } else {
                            byte[] addbytes = new byte[image_data.length + tmp.length];
                            System.arraycopy(tmp, 0, addbytes, image_data.length, tmp.length);
                            Log.e(TAG, "image2 : " + image_data);
                            image_data = addbytes;
                        }
                    } else {
                        Log.e(TAG, "브레이크!");
                        Toast.makeText(MainActivity.this, "끝", Toast.LENGTH_SHORT).show();
                        // 합친 문자열 비트맵 형변환
                        final Bitmap bm = byteToBitmap(image_data);
                        Log.d(TAG, "image size : " + image_data.length);
                        // 비트맵 이미지 imageView로 설정
                        runOnUiThread(new Runnable() {
                            public void run() {
                                ImgView.setImageBitmap(bm);
                            }
                        });

                        break;
                    }

                    /*// 바이트 데이터 스트링 형변환
                    final String tmp = new String(buffer, 0, size);
                    imgStr += tmp;

                    // 합친 문자열 비트맵 형변환
                    final Bitmap bm = StringToBitMap(imgStr);*/

                    // 비트맵 이미지 imageView로 설정
//                    runOnUiThread(new Runnable() {
//                        public void run() {
//                            ImgView.setImageBitmap(bm);
//
//                        }
//                    });

                }
            } catch (IOException e) {
                e.printStackTrace();
                Log.e(TAG, "수신 에러");
            }


        }

    }


    // fixme: Socket Connect.
    class ConnectThread extends Thread {
        String hostname;
        InputStream in;

        public ConnectThread(String addr) {
            hostname = addr;
        }

        public void run() {
            try { //클라이언트 소켓 생성

                int port = 9999;
                socket = new Socket(hostname, port);
                Log.d(TAG, "Socket 생성, 연결.");

                in = socket.getInputStream();

                Toptext = findViewById(R.id.text1);

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        InetAddress addr = socket.getInetAddress();
                        String tmp = addr.getHostAddress();
                        Toptext.setText(tmp + " 연결 완료");
                        Toast.makeText(getApplicationContext(), "Connected", Toast.LENGTH_LONG).show();

                        DiconButton.setEnabled(true);
                        ConnButton.setEnabled(false);
                        StartButton.setEnabled(true);
                    }
                });


            } catch (UnknownHostException uhe) { // 소켓 생성 시 전달되는 호스트(www.unknown-host.com)의 IP를 식별할 수 없음.

                Log.e(TAG, " 생성 Error : 호스트의 IP 주소를 식별할 수 없음.(잘못된 주소 값 또는 호스트 이름 사용)");
                runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Error : 호스트의 IP 주소를 식별할 수 없음.(잘못된 주소 값 또는 호스트 이름 사용)", Toast.LENGTH_SHORT).show();
                        Toptext.setText("Error : 호스트의 IP 주소를 식별할 수 없음.(잘못된 주소 값 또는 호스트 이름 사용)");
                    }
                });

            } catch (IOException ioe) { // 소켓 생성 과정에서 I/O 에러 발생.

                Log.e(TAG, " 생성 Error : 네트워크 응답 없음");
                runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Error : 네트워크 응답 없음", Toast.LENGTH_SHORT).show();
                        Toptext.setText("네트워크 연결 오류");
                    }
                });


            } catch (SecurityException se) { // security manager에서 허용되지 않은 기능 수행.

                Log.e(TAG, " 생성 Error : 보안(Security) 위반에 대해 보안 관리자(Security Manager)에 의해 발생. (프록시(proxy) 접속 거부, 허용되지 않은 함수 호출)");
                runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Error : 보안(Security) 위반에 대해 보안 관리자(Security Manager)에 의해 발생. (프록시(proxy) 접속 거부, 허용되지 않은 함수 호출)", Toast.LENGTH_SHORT).show();
                        Toptext.setText("Error : 보안(Security) 위반에 대해 보안 관리자(Security Manager)에 의해 발생. (프록시(proxy) 접속 거부, 허용되지 않은 함수 호출)");
                    }
                });


            } catch (IllegalArgumentException le) { // 소켓 생성 시 전달되는 포트 번호(65536)이 허용 범위(0~65535)를 벗어남.

                Log.e(TAG, " 생성 Error : 메서드에 잘못된 파라미터가 전달되는 경우 발생.(0~65535 범위 밖의 포트 번호 사용, null 프록시(proxy) 전달)");
                runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(getApplicationContext(), " Error : 메서드에 잘못된 파라미터가 전달되는 경우 발생.(0~65535 범위 밖의 포트 번호 사용, null 프록시(proxy) 전달)", Toast.LENGTH_SHORT).show();
                        Toptext.setText("Error : 메서드에 잘못된 파라미터가 전달되는 경우 발생.(0~65535 범위 밖의 포트 번호 사용, null 프록시(proxy) 전달)");
                    }
                });
            }
        }
    }


    @Override
    protected void onStop() {  //앱 종료시
        super.onStop();
        try {
            socket.close(); //소켓을 닫는다.
            Toptext.setText("연결 종료됨");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}