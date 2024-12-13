import baseURL from '@/service/service-axios-config';

const RoomService = {
    async getRoomList (data = {}){
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('room/list', {
            headers: {
                'Authorization': 'Bearer ' + accessToken
            },
            params: data
        })
    },
}

export default RoomService