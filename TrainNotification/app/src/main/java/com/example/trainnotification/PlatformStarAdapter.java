package com.example.trainnotification;

import android.app.Activity;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;


public class PlatformStarAdapter extends RecyclerView.Adapter<PlatformStarAdapter.MyViewHolder> {
    private MainActivity activity;
    private ArrayList<String> platformList;

    // 생성자
    public PlatformStarAdapter(Activity activity, ArrayList<String> platformList){
        this.activity = (MainActivity) activity;
        this.platformList = platformList;
    }

    // 리사이클러 뷰의 각 뷰에 들어갈 아이템들을 지정, 각 뷰는 뷰 홀더가 관여한다. 연결이 어댑터
    public class MyViewHolder extends  RecyclerView.ViewHolder {
        private TextView platform_name;
        private ImageView star;

        public MyViewHolder(View view) {
            super(view);
            this.platform_name = view.findViewById(R.id.item_platform_star_name);
            this.star = view.findViewById(R.id.item_platform_star_star);
        }
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_platform_star, parent, false);
        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull final MyViewHolder holder, final int position) {
        holder.star.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                activity.platform_fragment.changeStarState(platformList.get(position));
            }
        });
        holder.platform_name.setText(platformList.get(position));
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(activity, PlatformDetailActivity.class);
                intent.putExtra("platform_name", platformList.get(position));
                activity.startActivity(intent);
            }
        });

    }

    @Override
    public int getItemCount() {
        return platformList.size();
    }



}
