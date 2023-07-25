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
@font-face {
  font-family: "Cabin";
  src: url('./assets/fonts/Cabin-VariableFont_wdth,wght.woff2');
}
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
body{
  margin:0 auto;
}
.page-background{
  background-image: url("./assets/background.png");
  background-attachment: fixed;
  background-size: cover;
  background-repeat: no-repeat ;
  background-color: rgb(160, 160, 160);
  position: absolute;
  min-width: 100vw;
  min-height: 100vh;
}
</style>
