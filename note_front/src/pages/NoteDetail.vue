<script>
import { defineComponent, ref } from 'vue'
import {getNote, editNote, deleteNote} from '../services/notesService'
import {useRoute, useRouter} from 'vue-router'

export default defineComponent({
    name:"NoteDetail",
    setup() {
        const title = ref("")
        const content = ref("")
        const route = useRoute()
        const router = useRouter()
        const noteId = route.params.noteId
        return {title, content, noteId, router}
    },
    methods:{
        onEditNote(e){
            e.preventDefault()
            editNote(this.noteId, {title:this.title, content: this.content})
            .then(data => {
                if(data.status === 200){
                    alert("Nota editada correctamente!")
                }
            })
            .catch(() => {
                alert("Error al editar la nota")})
        },
        onDeleteNote(){
            deleteNote(this.noteId)
            this.router.push("/")
        }
    },
    created(){
        getNote(this.noteId)
        .then(data => {
            this.title = data.data.note.title,
            this.content = data.data.note.content
        })
    }
})
</script>

<template>
    <form class = "note-detail-form" @submit="editNote">
        <label>Titulo:</label>
        <input class = "input-title" type="text" :value= "title" @change="e => title=e.target.value"/>
        <label>Content:</label>
        <textarea class = "input-content" :value = "content" @change="e => content=e.target.value"></textarea>
        <div class = "buttons-container">
            <button class = "delete-button" @click="onDeleteNote()">Eliminar</button>
            <button class = "send-button" @click="onDeleteNote">Enviar</button>
        </div>
    </form>
</template>

<style scoped>
    .note-detail-form{
        width: 50vw;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap:10px;
    }
    .note-detail-form label{
        text-align: start;
    }
    .input-title{
        width: 99.8%;
    }
    .input-content{
        min-width: 100%;
        max-width: 100%;
        min-height: 100px;
    }
    .buttons-container{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .send-button{
        background-color:blue;
    }
    .delete-button{
        background-color:red;
    }
</style>
