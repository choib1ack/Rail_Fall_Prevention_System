package com.example.trainnoti2;

import android.graphics.Bitmap;

public class NotiDTO {

    private String datetime;
    private String location;
    private String image_name;
    private Boolean isChecked;

    public NotiDTO() {   }

    public NotiDTO(String datetime, String location, String image_name, Boolean isChecked) {
        this.datetime = datetime;
        this.location = location;
        this.image_name = image_name;
        this.isChecked = isChecked;
    }

    public String getDatetime() {
        return datetime;
    }

    public void setDatetime(String datetime) {
        this.datetime = datetime;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getImage_name() {
        return image_name;
    }

    public void setImage_name(String image_name) {
        this.image_name = image_name;
    }

    public Boolean getChecked() {
        return isChecked;
    }

    public void setChecked(Boolean checked) {
        isChecked = checked;
    }
}
