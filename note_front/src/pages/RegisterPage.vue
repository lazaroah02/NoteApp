<script>
import { defineComponent, ref } from 'vue'
import {register} from '../services/authentication'
import {useRouter} from "vue-router"
import './commonStyles/loginRegisterStyles.css'
import LoaderComponent from '../components/LoaderComponent'

export default defineComponent({
    setup() {
        const username = ref("")
        const email = ref("")
        const pass1 = ref("")
        const pass2 = ref("")
        const router = useRouter()
        const loading= ref(false)
        return {username, email, pass1, pass2, router, loading}
    },
    components:{
        LoaderComponent,
    },
    methods:{
        handleRegister(e){
            e.preventDefault();
            if(this.username === "" || this.email === "" || this.pass1 === "" || this.pass2 === ""){
                alert("Don't leave empty fields")
            }
            else if(this.pass1 != this.pass2){
                alert("Passwords not the same")
            }
            else{
                this.loading = true
                register({username:this.username, email:this.email, password1: this.pass1, password2: this.pass2})
                .then(data => {
                    console.log(data)
                    if(data.data.register.success){
                        localStorage.setItem("jwt", data.data.register.token)
                        this.$store.commit("fetchInfoUser", {token:data.data.register.token})
                        this.loading = false
                        this.router.push("/")
                    }
                    else{
                        this.loading = false
                        if(data.data.register.errors.email){
                            alert(data.data.register.errors.email[0].message)
                        }
                        else if(data.data.register.errors.password2){
                            alert("Check the password, is too common, too short or too easy")
                        }
                        else{
                            alert("Error in register")
                        }
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
            </div>
            <form @submit="e => handleRegister(e)" class = "form register-form">
                <label >Username</label>
                <input type="text" :value = "username" @change = "e => username = e.target.value"/>
                <label >Email</label>
                <input type="email" :value = "email" @change = "e => email = e.target.value"/>
                <label>Password</label>
                <input type="text" :value = "pass1" @change = "e => pass1 = e.target.value"/>
                <label>Repeat Password</label>
                <input type="text" :value = "pass2" @change = "e => pass2 = e.target.value"/>
                <div class = "register-link">If you have account login <a @click="router.push('/login')">here</a></div>
                <button>{{!loading?"Register":null}}
                    <div v-if="loading" class = "login-loader-component"><LoaderComponent/></div>
                </button>
            </form>
        </div>
    </div>
</template>

