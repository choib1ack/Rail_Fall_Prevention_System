package com.example.trainnotification;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.util.ArrayList;


public class NotificationListAdapter extends RecyclerView.Adapter<NotificationListAdapter.MyViewHolder> {

    private ArrayList<NotiDTO> notification_list;
    private NotificationListActivity activity;
    FirebaseStorage storage = FirebaseStorage.getInstance();
    StorageReference storageRef = storage.getReference();

    // 생성자
    public NotificationListAdapter(Activity activity, ArrayList<NotiDTO> notification_list){
        this.activity = (NotificationListActivity) activity;
        this.notification_list = notification_list;
    }

    // 리사이클러 뷰의 각 뷰에 들어갈 아이템들을 지정, 각 뷰는 뷰 홀더가 관여한다. 연결이 어댑터
    public class MyViewHolder extends  RecyclerView.ViewHolder {
        private TextView datetime;
        private TextView location;
        private Button ischecked;
        private ImageView image;

        public MyViewHolder(View view) {
            super(view);
            this.datetime = view.findViewById(R.id.notilist_datetime);
            this.location = view.findViewById(R.id.notilist_location);
            this.ischecked = view.findViewById(R.id.notilist_ischecked);
            this.image = view.findViewById(R.id.notilist_image);
        }
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_noti_list, parent, false);
        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull final MyViewHolder holder, final int position) {
        holder.datetime.setText(notification_list.get(position).getDatetime());
        holder.location.setText("["+notification_list.get(position).getLocation()+"] 위험이 감지되었습니다.");

        if(notification_list.get(position).getChecked() == false){ // 사용자가 알림을 확인하지 않았다면
            holder.ischecked.setVisibility(View.VISIBLE); // 파랑 동그라미 보이게
        }else{
            holder.ischecked.setVisibility(View.INVISIBLE); // 안보이게
        }

        String image_file_name = notification_list.get(position).getImage_name();

        StorageReference pathReference = storageRef.child(image_file_name);

        pathReference.getDownloadUrl().addOnCompleteListener(new OnCompleteListener<Uri>() {
            @Override
            public void onComplete(@NonNull Task<Uri> task) {
                if (task.isSuccessful()) {
                    Glide.with(activity)
                            .load(task.getResult())
                            .into(holder.image);
                    if(position == getItemCount()-1){
                        activity.loading_circle.setVisibility(View.GONE); // 사진 로딩이 끝나면 로딩중 표시 지우기
                    }
                } else {
                    Toast.makeText(activity, task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                }
            }
        });
//        if(position == getItemCount()-1){
//            activity.dashboard_fragment.loading_circle.setVisibility(View.GONE);
//        }

        holder.itemView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(activity, NotificationDetailActivity.class);
                intent.putExtra("location", notification_list.get(position).getLocation());
                intent.putExtra("datetime", notification_list.get(position).getDatetime());
                activity.startActivity(intent);
            }
        });
    }

    @Override
    public int getItemCount() {
        return notification_list.size();
    }

}
