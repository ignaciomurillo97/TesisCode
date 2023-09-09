import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

// Use ElementPlus
app.use(ElementPlus)

// Mount the app
app.mount('#app')