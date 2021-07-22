import { createApp } from 'vue'
import App from './App.vue'
import 'bulma/css/bulma.css'
import router from './router.js'
import Repo from "@/repo/repo.js"

const app = createApp(App)
app.use(router)
app.provide('$http', new Repo()); 
app.mount('#app')

