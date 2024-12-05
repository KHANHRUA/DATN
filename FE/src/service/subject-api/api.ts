import baseURL from '@/service/service-axios-config';

const SubjectService = {
    async GetSubject (query) {
        return await baseURL.get('subject/list',{
            params: query
        })
    },
}

export default SubjectService;