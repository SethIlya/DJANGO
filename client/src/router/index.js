import { createRouter, createWebHistory } from 'vue-router';
import App from '@/App.vue';
import GenresView from '../views/GenresView.vue';
import StudioView from '../views/StudioView.vue';
import DirectorView from '../views/DirectorView.vue';
import PlatformView from '../views/PlatformView.vue';
import GamesView from '../views/GamesView.vue';
import TestView from '../views/TestView.vue';
const routes = [
 {
  path: '/',
  name: 'Games',
  component: GamesView,  
 },
 {
  path: '/test',
  name: 'Test',
  component: TestView,
 },
 {
  path: '/genres',
  name: 'Genres',
  component: GenresView,
 },
 {
  path: '/studio',
  name: 'Studio',
  component: StudioView,
 },
 {
  path: '/director',
  name: 'Director',
  component: DirectorView,
 },
 {
  path: '/platform',
  name: 'Platform',
  component: PlatformView,
 }
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})
export default router;
