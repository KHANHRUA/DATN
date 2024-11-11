import baseURL from '@/service/service-axios-config';

const ClassService = {
    async getAllClasses (name: string){
        const accessToken = localStorage.getItem('token')
        return await baseURL.get('class/list',{
            headers: {
                'Authorization': 'Bearer ' + accessToken
            },
            params:{
                name : name ?? null
            }
        })
    },
}

export default ClassService