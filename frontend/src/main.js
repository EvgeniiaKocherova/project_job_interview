import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // <--- Импортируем роутер

const app = createApp(App)

app.use(router) // <--- ГОВОРИМ VUE ИСПОЛЬЗОВАТЬ РОУТЕР
app.mount('#app')