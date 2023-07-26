<script>
import { defineComponent, ref } from 'vue'
import {getNote, editNote, deleteNote} from '../services/notesService'
import {useRoute, useRouter} from 'vue-router'
import './commonStyles/pages.css'
import './commonStyles/addNote-editNote-styles.css'

export default defineComponent({
    name:"NoteDetail",
    setup() {
        const title = ref("")
        const content = ref("")
        const showErrorMessage = ref(false)
        const route = useRoute()
        const router = useRouter()
        const noteId = route.params.noteId
        return {title, content, noteId, router, showErrorMessage}
    },
    methods:{
        handleEditNote(e){
            e.preventDefault()
            editNote({noteId: this.noteId, token:this.userToken, data:{title:this.title, content: this.content}})
            .then(data => {
                if(data.errors){
                    alert("Error al editar la nota")
                }else{
                    alert("Nota editada correctamente!")
                }
            })
        },
        handleDeleteNote(){
            deleteNote({noteId:this.noteId, token:this.userToken})
            .then((data) => {
                if(data.errors){
                    alert("Error al eliminar la nota")
                }else{
                    this.router.push("/")
                }
            })
        },
        fetchNote(token){
            if(token){
                getNote({noteId:this.noteId, token:this.userToken})
                .then(data => {
                    if(data.errors){
                        this.showErrorMessage = true
                    }else{
                        this.title = data.data.note.title,
                        this.content = data.data.note.content
                    }
                })
            }
        }
    },
    //watch when user token change to fecth user notes
    computed:{
        userToken(){
            return this.$store.state.infoUser.token
        }
    },
    watch:{
        userToken(token){
            this.fetchNote(token)
        }
    },
    mounted(){
        this.fetchNote(this.userToken)
    }
})
</script>

<template>
    <div class = "page-background">
        <div class = "panel">
            <div class = "title"><span>Green</span> Notes</div>
            <form v-if="!showErrorMessage"  class = "note-form" @submit="(e) => handleEditNote(e)">
                <div class = "go-back-button-and-input-title-container">
                    <button 
                        class = "go-back-button" 
                        type = "button"
                        @click="router.push('/')"
                        ><img alt = "chevron-left" src = "../assets/chevron-left.svg"/></button>
                        <input class = "input-title" type="text" :value= "title" @change="e => title=e.target.value"/>
                </div>
                <textarea class = "input-content" :value = "content" @change="e => content=e.target.value"></textarea>
                <button type = "button" class = "cancel-button" @click="handleDeleteNote()"><img alt = "trash" src = "../assets/trash.svg"/></button>
                <button class = "send-button"><img alt = "check" src = "../assets/check-icon.svg"/></button>
            </form>
            <div v-else class = "error-message">Error to get the note</div>
        </div>
    </div>
</template>

<style scoped>
    .error-message{
        width: 200px;
        background-color:#DC6161;
        margin:0 auto;
        position:relative;
        right: 20px;
        top:80vh;
        color:white;
        text-align:center;
        border-radius: 10px;
        height: 30px;
        font-family: 'Raleway';
        padding-top: 10px;
    }
</style>
