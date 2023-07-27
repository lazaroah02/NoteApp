<script>
import { defineComponent, ref } from 'vue'
import {login} from '../services/authentication'
import {useRouter} from "vue-router"
import './commonStyles/loginRegisterStyles.css'
import LoaderComponent from '../components/LoaderComponent'

export default defineComponent({
    setup() {
        const username = ref("")
        const password = ref("")
        const router = useRouter()
        const loading = ref(false)
        return {username, password, router, loading}
    },
    components:{
        LoaderComponent,
    },
    methods:{
        handleLogin(e){
            e.preventDefault();
            if(this.username === "" || this.password === ""){
                alert("Don't leav empty fields")
            }
            else{
                this.loading = true
                login({username:this.username, password: this.password})
                .then(data => {
                    if(data.data.tokenAuth.success === true){
                        localStorage.setItem("jwt", data.data.tokenAuth.token)
                        this.$store.commit("setInfoUser", {username:this.username, token:data.data.tokenAuth.token})
                        this.loading = false
                        this.router.push("/")
                    }
                    else{
                        this.loading = false
                        alert("Error in login, check your password or username")
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
                <button>{{!loading?"Login":null}}
                    <div class = "login-loader-component" v-if="loading"><LoaderComponent/></div>
                </button>
            </form>
        </div>
    </div>
</template>
