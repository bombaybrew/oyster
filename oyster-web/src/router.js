import {
    createWebHashHistory,
    createRouter
} from "vue-router";
import Home from "@/views/Home.vue";
import About from "@/views/About.vue"
import Docs from "@/views/Docs.vue";

const routes = [{
        path: '/',
        component: Home
    },
    {
        path: '/docs',
        component: Docs
    },
    {
        path: '/about',
        component: About
    },
]


const router = createRouter({
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

export default router;