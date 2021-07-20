import {
    createWebHashHistory,
    createRouter
} from "vue-router";
import Home from "@/ui/Home.vue";

const routes = [{
    path: '/',
    component: Home
}, ]


const router = createRouter({
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

export default router;