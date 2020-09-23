package com.example.trainnoti2;

public class DangerDTO {
    private String id;
    private String datetime;
    private String location;
    private String state;
    private String image_name;

    public DangerDTO() {   }

    public DangerDTO(String id, String datetime, String location, String state, String image_id) {
        this.id = id;
        this.datetime = datetime;
        this.location = location;
        this.state = state;
        this.image_name = image_id;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
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

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getImage_name() {
        return image_name;
    }

    public void setImage_name(String image_id) {
        this.image_name = image_id;
    }
}
