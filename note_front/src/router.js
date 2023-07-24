import {createRouter, createWebHashHistory} from 'vue-router';

const routes = [
  {
    path: '/',
    redirect: "/notes"
  },
  {
    name:"NotesList",
    path: '/notes',
    component:() => import('./pages/NotesList.vue'),
  },
  {
    name:"NoteDetail",
    path: '/note/:noteId',
    component: () => import('./pages/NoteDetail.vue'),
  },
  {
    name:"AddNote",
    path: '/notes/add/',
    component: () => import('./pages/AddNote.vue'),
  },
  {
    path:"/:pathMatch(.*)*",
    component:() => import('./pages/NotFound.vue'),
  },
  {
    path:"/login",
    component:() => import('./pages/LoginPage.vue'),
  },
  {
    path:"/register",
    component:() => import('./pages/RegisterPage.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes, 
})

export default router

