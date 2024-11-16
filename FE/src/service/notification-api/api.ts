import baseURL from '@/service/service-axios-config';
import type {Notification} from "@/interface/notification"

const NotificationService = {
    async CreateNotification (data: Notification){
        const accessToken = localStorage.getItem('token')
        return await baseURL.put('notification/create',
            data
        ,{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
    },

    async getNotification (data = {}){
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('notification/list', {
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                },
                params: data
            })
    },
}

export default NotificationService