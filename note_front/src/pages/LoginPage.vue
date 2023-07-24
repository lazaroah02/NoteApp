<script>
import { defineComponent, ref } from 'vue'
import {login} from '../services/authentication'
import {useRouter} from "vue-router"

export default defineComponent({
    setup() {
        const username = ref("")
        const password = ref("")
        const router = useRouter()
        return {username, password, router}
    },
    methods:{
        handleLogin(e){
            e.preventDefault();
            if(this.username === "" || this.password === ""){
                alert("No deben haber campos vacios")
            }
            else{
                login({username:this.username, password: this.password})
                .then(data => {
                    if(data.data.tokenAuth.success === true){
                        localStorage.setItem("jwt", data.data.tokenAuth.token)
                        this.router.push("/")
                    }
                    else{
                        alert("Error al iniciar sesion")
                    }
                })
            }
        }
    }
})
</script>

<template>
    <div>
        <form @submit="e => handleLogin(e)">
            <label>Username</label>
            <input type="text" placeholder="Username" :value = "username" @change = "e => username = e.target.value"/>
            <label>Password</label>
            <input type="text" placeholder="Password" :value = "password" @change = "e => password = e.target.value"/>
            <button>Login</button>
        </form>
    </div>
</template>
