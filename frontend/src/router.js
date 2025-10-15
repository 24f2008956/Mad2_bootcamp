import { createRouter,createWebHistory } from "vue-router";
//import components here that are to be routed
import login from './components/LoginComp.vue';
import HomeComp from './components/HomeComp.vue';
import RegisterComp from './components/RegisterComp.vue';
import admindashboard from './pages/admindashboard.vue';
import userdashboard from './pages/userdashboard.vue';
import parkinglots from "./components/parking_lot.vue";
import EditLot from "./components/edit_lot.vue";
//import CreateLot from "./components/create_lot.vue";
const routes = [
    {path:"/", component: HomeComp},
    {path:"/login", component: login},
    {path:"/register", component: RegisterComp},
    {path: "/admin/dashboard",component: admindashboard,
        children: [
            {
            path: "parkinglot",
            component: parkinglots
            }
        
           
        ]
    },
    {path: '/admin/parking_lots/:id/edit', component: EditLot, props: true},
    {path:"/user/dashboard", component:userdashboard}
]


const router= createRouter({
    history: createWebHistory(),

    routes
})

export default router;