import { createApp } from 'vue'
import App from './App.vue'
import Main from "@/components/Main.vue";
import {createRouter, createWebHistory} from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: App },
        { path: '/main', component: Main }
    ]
});

const app = createApp(App)

app.use(router)

app.mount('#app')
