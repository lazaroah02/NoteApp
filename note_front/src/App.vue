<template>
  <router-view />
</template>

<script>
import { useRouter } from 'vue-router'
import { isLoggedIn } from './utils/checkUserIsLoggedIn'

export default {
  name: 'App',
  setup(){
    const router = useRouter()
    return {router}
  },
  methods:{
    addCont(){
      this.$store.commit("increment", {value:2})
    }
  },
  mounted(){
    let token = isLoggedIn()
    if(token){
      this.$store.commit("fetchInfoUser", {token:token})
    }
    else{
      this.router.push("/login")
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
