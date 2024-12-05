import baseURL from '@/service/service-axios-config';

const SessionService = {
    async GetSession (query) {
        return await baseURL.get('session/list',{
            params: query
        })
    },

    async CreateSession (data) {
        const accessToken = localStorage.getItem('token')
        return await baseURL.put('session/create',data,{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
    },

    async CreateMultipleSession (data) {
        const accessToken = localStorage.getItem('token')
        return await baseURL.put('session/create-multiple',data,{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
    },
}

export default SessionService;