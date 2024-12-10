import {ROLES} from "@/utils/constant";

export interface User {
    id: number;
    name: string;
    age: number;
    gender_id: number;
    class_id: number;
    face_image: string;
    role: string;
    subject: number[]
}

export interface FilterUser {
    name: string,
    role: ROLES
}

export interface UserData {
    id: number;
    name?: string;
    age?: number;
    gender_id?: number;
    fileList?: object;
    class_id?: number;
    face_image?:string;
    role?: string;
    subject?: number[]
}