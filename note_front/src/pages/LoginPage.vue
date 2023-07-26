<script>
import { defineComponent, ref } from 'vue'
import {login} from '../services/authentication'
import {useRouter} from "vue-router"
import './commonStyles/loginRegisterStyles.css'

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
                alert("Don't leav empty fields")
            }
            else{
                login({username:this.username, password: this.password})
                .then(data => {
                    if(data.data.tokenAuth.success === true){
                        localStorage.setItem("jwt", data.data.tokenAuth.token)
                        this.$store.commit("setInfoUser", {username:this.username, token:data.data.tokenAuth.token})
                        this.router.push("/")
                    }
                    else{
                        alert("Error in login")
                    }
                })
            }
        }
    }
})
</script>

<template>
    <div class = "page-background">
        <div class = "login-register-panel">
            <div class = "title-container">
                <div class = "title">Welcome to <span> Green</span> Notes <img alt = "notes-logo" src = "../assets/logo.png"/></div>
                <div class = "description">
                    <span>Hello, in Green Notes you can</span>
                    <span>save notes in a simple,</span>
                    <span>easy and safe way</span>
                </div>
            </div>
            <form @submit="e => handleLogin(e)" class = "form">
                <label >Username</label>
                <input type="text" :value = "username" @change = "e => username = e.target.value"/>
                <label>Password</label>
                <input type="text" :value = "password" @change = "e => password = e.target.value"/>
                <div class = "register-link">If you don't have account register <a @click="router.push('/register')">here</a></div>
                <button>Login</button>
            </form>
        </div>
    </div>
</template>
