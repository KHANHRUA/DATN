import axiosBase from "axios";

const baseURL = axiosBase.create({
    // This is base
    baseURL: 'http://localhost:5000/api/',
    timeout: 30000,
    headers: {},
});


export default baseURL;