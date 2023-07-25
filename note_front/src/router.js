import {createRouter, createWebHashHistory} from 'vue-router';

const routes = [
  {
    name:"NotesList",
    path: '/',
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
    name:"Register",
    path:"/register",
    component:() => import('./pages/RegisterPage.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes, 
})

export default router

