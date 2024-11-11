import {ElMessage} from "element-plus";

interface option {
    message: string
    type: type
}

enum type {
    'success',
    'warning' ,
    'info' ,
    'error'
}

export function customMessage(option){
    ElMessage({
        message: option.message,
        type: option.type,
        duration: option.duration || 1000
    });
}