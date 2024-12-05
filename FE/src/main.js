import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import ElementPlus from 'element-plus';
import {customMessage} from "@/utils/message.ts";
import 'element-plus/dist/index.css';
import {ROLE} from '@/store/store.ts';
import '@/scss/glocal.scss'
import _ from 'lodash';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

const app = createApp(App)

app.use(ElementPlus)

app.use(router)

app.use(ROLE)

app.use(_)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}

app.config.globalProperties.$message = customMessage

app.mount('#app');