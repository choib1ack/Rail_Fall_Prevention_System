package com.example.trainnoti2;

import android.app.Activity;
import android.content.Intent;
import android.media.Image;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.util.ArrayList;


public class DashboardAdapter2 extends RecyclerView.Adapter<DashboardAdapter2.MyViewHolder> {

    private ArrayList<DangerDTO> dangerData;
    private MainActivity activity;
    FirebaseStorage storage = FirebaseStorage.getInstance();
    StorageReference storageRef = storage.getReference();

    // 생성자
    public DashboardAdapter2(Activity activity, ArrayList<DangerDTO> dangerData){
        this.activity = (MainActivity) activity;
        this.dangerData = dangerData;
    }

    // 리사이클러 뷰의 각 뷰에 들어갈 아이템들을 지정, 각 뷰는 뷰 홀더가 관여한다. 연결이 어댑터
    public class MyViewHolder extends  RecyclerView.ViewHolder {
        private TextView datetime;
        private TextView location;
        private Button state;
        private ImageView image;

        public MyViewHolder(View view) {
            super(view);
            this.datetime = view.findViewById(R.id.dash_datetime2);
            this.location = view.findViewById(R.id.dash_location2);
            this.state = view.findViewById(R.id.dash_state_btn2);
            this.image = view.findViewById(R.id.dash_image2);
        }
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_danger_chatformat, parent, false);
        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull final MyViewHolder holder, final int position) {
        holder.datetime.setText(dangerData.get(position).getDatetime());
        holder.location.setText(dangerData.get(position).getLocation());

        if(dangerData.get(position).getState().equals("미처리")){
            holder.state.setText(dangerData.get(position).getState());
            holder.state.setBackground(ContextCompat.getDrawable(activity, R.drawable.button_state_no));
        }else{
            holder.state.setText("처리완료");
            holder.state.setBackground(ContextCompat.getDrawable(activity, R.drawable.button_state_ok));
        }

        String image_file_name = dangerData.get(position).getImage_name();
//        image.setImageBitmap(intent.get("status"));

        StorageReference pathReference = storageRef.child(image_file_name);

        pathReference.getDownloadUrl().addOnCompleteListener(new OnCompleteListener<Uri>() {
            @Override
            public void onComplete(@NonNull Task<Uri> task) {
                if (task.isSuccessful()) {
                    Glide.with(activity)
                            .load(task.getResult())
                            .into(holder.image);
                    if(position == getItemCount()-1){
                        activity.dashboard_fragment.loading_circle.setVisibility(View.GONE);
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
                Intent intent = new Intent(activity, DetailActivity.class);
                intent.putExtra("location", dangerData.get(position).getLocation());
                intent.putExtra("datetime", dangerData.get(position).getDatetime());
                intent.putExtra("status", dangerData.get(position).getState());
                intent.putExtra("image_name", dangerData.get(position).getImage_name());
                activity.startActivity(intent);
            }


        });

    }

    @Override
    public int getItemCount() {
        return dangerData.size();
    }



}
