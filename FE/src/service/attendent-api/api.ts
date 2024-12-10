import baseURL from '@/service/service-axios-config';

const AttendantService = {
    async GetAttendant (query) {
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('attendant/list',{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            },
            params: query
        })
    },
}

export default AttendantService;