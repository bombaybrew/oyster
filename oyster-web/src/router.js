import {
    createWebHashHistory,
    createRouter
} from "vue-router";
import Home from "@/views/Home.vue";
import About from "@/views/About.vue"
import Docs from "@/views/Docs.vue";
import ModelCreate from "@/views/ModelCreate.vue"
import DataLoad from "@/views/DataLoad.vue"
import EditDataset from "@/views/EditDataset.vue"

const routes = [{
        path: '/',
        component: Home
    },
    {
        path: '/create',
        component: ModelCreate
    },
    {
        name: 'dataset',
        path: '/dataset',
        component: EditDataset,
        props: true
    },
    {
        path: '/dataload',
        component: DataLoad
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