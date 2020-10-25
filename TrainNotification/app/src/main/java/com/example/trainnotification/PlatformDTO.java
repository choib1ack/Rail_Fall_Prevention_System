package com.example.trainnotification;

import java.util.ArrayList;

public class PlatformDTO {
    private String platform_name;
    private ArrayList<DangerDTO> dangerList_of_platform;

    public PlatformDTO() {}

    public PlatformDTO(String platform_name, ArrayList<DangerDTO> dangerList_of_platform) {
        this.platform_name = platform_name;
        this.dangerList_of_platform = dangerList_of_platform;
    }

    public String getPlatform_name() {
        return platform_name;
    }

    public void setPlatform_name(String platform_name) {
        this.platform_name = platform_name;
    }

    public ArrayList<DangerDTO> getDangerList_of_platform() {
        return dangerList_of_platform;
    }

    public void setDangerList_of_platform(ArrayList<DangerDTO> dangerList_of_platform) {
        this.dangerList_of_platform = dangerList_of_platform;
    }
}
