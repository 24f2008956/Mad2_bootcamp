import { createRouter,createWebHistory } from "vue-router";
//import components here that are to be routed
import login from './components/LoginComp.vue';
import HomeComp from './components/HomeComp.vue';
import RegisterComp from './components/RegisterComp.vue';
import Dashboard from "./components/dashboard.vue";

const routes = [
    {path:"/", component: HomeComp},
    {path:"/login", component: login},
    {path:"/register", component: RegisterComp},
    {path:"/dashboard", component:Dashboard}

]


const router= createRouter({
    history: createWebHistory(),

    routes
})

export default router;