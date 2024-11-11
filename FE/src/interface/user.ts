import {ROLES} from "@/utils/constant";

export interface User {
    id: number;
    name: string;
    age: number;
    gender_id: number;
    class_id: number;
    face_image: string;
    role: string;
}

export interface FilterUser {
    name: string,
    role: ROLES
}