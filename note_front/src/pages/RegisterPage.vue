<script>
import { defineComponent, ref } from 'vue'
import {register} from '../services/authentication'
import {useRouter} from "vue-router"

export default defineComponent({
    setup() {
        const username = ref("")
        const email = ref("")
        const pass1 = ref("")
        const pass2 = ref("")
        const router = useRouter()
        return {username, email, pass1, pass2, router}
    },
    methods:{
        handleRegister(e){
            e.preventDefault();
            if(this.username === "" || this.email === "" || this.pass1 === "" || this.pass2 === ""){
                alert("No deben haber campos vacios")
            }
            if(this.pass1 != this.pass2){
                alert("Las contraseñas no son iguales")
            }
            else{
                register({username:this.username, email:this.email, password1: this.pass1, password2: this.pass2})
                .then(data => {
                    if(data.data.tokenAuth.success === true){
                        this.router.push("/notes")
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
            <label>Email</label>
            <input type="text" placeholder="Email" :value = "username" @change = "e => username = e.target.value"/>
            <label>Password1</label>
            <input type="text" placeholder="Password" :value = "password" @change = "e => password = e.target.value"/>
            <label>Password2</label>
            <input type="text" placeholder="Password" :value = "password" @change = "e => password = e.target.value"/>
            <button>Register</button>
        </form>
    </div>
</template>
