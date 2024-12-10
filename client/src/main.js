import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import "bootstrap/dist/js/bootstrap"

import App from './App.vue'
import router from './router'

// import GenresView from './views/GenresView.vue'
// import StudioView from './views/StudioView.vue'
// import DirectorView from './views/DirectorView.vue'
// import PlatformView from './views/PlatformView.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')