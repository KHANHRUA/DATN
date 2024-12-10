import baseURL from '@/service/service-axios-config';

import { LoginParam } from "@/interface/login";
import {UserData} from "@/interface/user";

const UserService = {
    async Login (data: LoginParam){
        return await baseURL.post('auth/login',data)
    },

    async Auth (){
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('auth/user-check',{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
    },

    async Register (data){
        return await baseURL.post('auth/register',data)
    },

    async DeleteUser (id)   {
        const accessToken = localStorage.getItem('token')
        return await baseURL.delete('/user/user-erase',{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            },
            params: {
                id: id
            }
        })
    },

    async GetGender () {
        return await baseURL.get('gender/list')
    },

    async GetRoles () {
        return await baseURL.get('user/roles')
    },

    async GetUsers (query = {}) {
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('user/list',
            {
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                },
                params:{
                    name: query.name ?? null,
                    role: query.role ?? null
                }
            })
    },

    async GetInformation () {
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('user/my-information',
            {
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                }
            })
    },

    async ChangeInformation (data: UserData) {
        const accessToken = localStorage.getItem('token')
        const id = data.id
        delete data.fileList;
        delete data.id;
        return await baseURL.patch(`user/change-info/${id}`,
            data,
            {
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                }
            })
    }
}

export default UserService