package com.example.trainnotification;

import android.app.Activity;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;


public class PlatformDetailAdapter extends RecyclerView.Adapter<PlatformDetailAdapter.MyViewHolder> {

    private ArrayList<DangerDTO> dangerData;
    private PlatformDetailActivity activity;

    // 생성자
    public PlatformDetailAdapter(Activity activity, ArrayList<DangerDTO> dangerData){
        this.activity = (PlatformDetailActivity) activity;
        this.dangerData = dangerData;
    }

    // 리사이클러 뷰의 각 뷰에 들어갈 아이템들을 지정, 각 뷰는 뷰 홀더가 관여한다. 연결이 어댑터
    public class MyViewHolder extends  RecyclerView.ViewHolder {
        private TextView datetime;
        private TextView location;
        private Button state;

        public MyViewHolder(View view) {
            super(view);
            this.datetime = view.findViewById(R.id.dash_datetime);
            this.location = view.findViewById(R.id.dash_location);
            this.state = view.findViewById(R.id.dash_state_btn);
        }
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_danger, parent, false);
        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, final int position) {
        holder.datetime.setText(dangerData.get(position).getDatetime());
        holder.location.setText(dangerData.get(position).getLocation());

        if(dangerData.get(position).getState().equals("미처리")){
            holder.state.setText(dangerData.get(position).getState());
            holder.state.setBackground(ContextCompat.getDrawable(activity, R.drawable.button_state_no));
        }else{
            holder.state.setText(dangerData.get(position).getState());
            holder.state.setBackground(ContextCompat.getDrawable(activity, R.drawable.button_state_ok));
        }
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
