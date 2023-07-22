<script>
import { defineComponent, ref} from 'vue'
import {getNotes, deleteNote} from '../services/notesService'
import {useRouter} from 'vue-router'

export default defineComponent({
    name:"NotesList",
    setup() {
        const notes = ref([])
        const router = useRouter()
        return {notes, router}
    },
    created(){
        getNotes()
        .then(data => {
            this.notes = data.data.notes})
    },
    methods:{
        validateLength(text){
            if(text.length > 30){
                return `${text.substring(0, 30)}...`
            }
            return text
        },
        handleDeleteNote(noteId){
            deleteNote(noteId)
            .then(message => {
                alert(message)
                this.removeNoteFromNoteList(noteId)
            })
            .catch(() => alert("Error al borrar la nota"))
        },
        removeNoteFromNoteList(noteId){
            for(let i = 0; i < this.notes.length; i++){
                if(this.notes[i].id == noteId){
                    this.notes.splice(i, 1)
                }
            }
        }
    }, 
})
</script>

<template>
    <button @click="router.push(to = '/notes/add')">Create Note</button>
    <div class = "cards-container">
        <div class = "card" v-for="note in notes" :key="note.id">
            <h4 class = "title">{{ validateLength(note.title) }}</h4>
            <div class = "content">{{ validateLength(note.content) }}</div>
            <div class = "buttons-container">
                <button class = "edit-button" @click="router.push(`note/${note.id}`)">Edit</button>
                <button class = "delete-button" @click="handleDeleteNote(note.id)">Delete</button>
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