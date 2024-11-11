import { createStore } from 'vuex';
import {ROLES} from "@/utils/constant";

const ROLE = createStore({
    state: {
        myRole: ROLES.STUDENT
    },
    mutations: {
        setRole(state: ROLES, newRole:ROLES) {
            state.myRole = newRole;
        }
    }
});

export {ROLE}