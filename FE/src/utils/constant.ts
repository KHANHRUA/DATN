const HTTPS_CODE = {
    SUCCESS: 200,
    BAD_REQUEST: 400,
    INTERNALS_SERVER_ERROR: 500,
    UNPROCESSABLE_ENTITY: 422,
    NOT_FOUND: 404,
    FORBIDDEN: 403,
    UNAUTHORIZED: 401,
};

const ROLES = {
    ADMIN: 'admin',
    TEACHER: 'teacher',
    STUDENT: 'student'
}

export { HTTPS_CODE, ROLES };
