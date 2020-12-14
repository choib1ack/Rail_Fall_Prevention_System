package com.example.trainnotification;

import java.util.ArrayList;

public class StarPlatformDTO {
    private ArrayList<String> star_platform_list;

    public StarPlatformDTO() {   }

    public StarPlatformDTO(ArrayList<String> star_platform_list) {
        this.star_platform_list = star_platform_list;
    }

    public ArrayList<String> getStar_platform_list() {
        return star_platform_list;
    }

    public void setStar_platform_list(ArrayList<String> star_platform_list) {
        this.star_platform_list = star_platform_list;
    }
}
