import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import BaseIcon from './components/BaseIcon.vue'

const app = createApp(App)

app.component('BaseIcon', BaseIcon)
app.use(router)

app.mount('#app')
