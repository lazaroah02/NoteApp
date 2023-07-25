<script>
import {ref} from 'vue'
import {getNotes, deleteNote} from '../services/notesService'
import {useRouter} from 'vue-router'

export default {
    name:"NotesList",
    setup() {
        const notes = ref([])
        const router = useRouter()

        return {notes, router}
    },
    methods:{
        validateLength(text){
            if(text.length > 30){
                return `${text.substring(0, 30)}...`
            }
            return text
        },
        handleDeleteNote(noteId){
            deleteNote({noteId:noteId, token:this.userToken})
            .then(data => {
                if(data.errors){
                    alert("Error al eliminar la nota")
                }
                else{
                    alert("Nota eliminada correctamente")
                    this.removeNoteFromNoteList(noteId)
                }
            })
            
        },
        removeNoteFromNoteList(noteId){
            for(let i = 0; i < this.notes.length; i++){
                if(this.notes[i].node.id == noteId){
                    this.notes.splice(i, 1)
                }
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
            if(token){
                getNotes({token:token})
                .then(data => {
                    this.notes = data.data.notes.edges
                })
            }
        },
    },
    mounted(){
        if(this.userToken){
            getNotes({token:this.userToken})
                .then(data => {
                    this.notes = data.data.notes.edges
                })
        }
    }
}
</script>

<template>
    <button @click="router.push(to = '/notes/add')">Create Note</button>
    <div class = "cards-container">
        <div class = "card" v-for="note in notes" :key="note.node.id">
            <h4 class = "title">{{ validateLength(note.node.title) }}</h4>
            <div class = "content">{{ validateLength(note.node.content) }}</div>
            <div class = "buttons-container">
                <button class = "edit-button" @click="router.push(`note/${note.node.id}`)">Edit</button>
                <button class = "delete-button" @click="handleDeleteNote(note.node.id)">Delete</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .cards-container{
        display: grid;
        width: 90vw;
        margin: 0 auto;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap:30px;
    }
    .card{
        border:1px solid;
        padding:10px;
        padding-top:0;
    }
    .title{
        text-align: start;
    }
    .content{
        display: flex;
        justify-content:flex-start;
    }
    .buttons-container{
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        position: relative;
        top:35px;
        gap:10px;
    }
    .delete-button{
        background-color:red;
    }
    .edit-button{
        background-color:blue;
    }
</style>