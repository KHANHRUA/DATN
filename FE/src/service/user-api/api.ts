import baseURL from '@/service/service-axios-config';

import { LoginParam } from "@/interface/login";

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
    }
}

export default UserService