<script>
    import { defineComponent, ref } from 'vue'
    import { createNote } from '../services/notesService';
    import {useRouter} from 'vue-router'

    export default defineComponent({
        name:"AddNote",
        setup(){
            const title = ref("")
            const content = ref("")
            const router = useRouter()
            return {title, content, router}
        },
        methods:{
            createNote(e){
                e.preventDefault();
                createNote({title:this.title, content:this.content})
                .then(() => {this.router.push("/")})
                .catch(() => alert("Error al crear la nota"))
            }
        }
    })
</script>

<template>
    <form class = "note-detail-form" @submit="createNote">
        <label>Titulo:</label>
        <input class = "input-title" type="text" @change="e => title = e.target.value"/>
        <label>Content:</label>
        <textarea class = "input-content" @change="e => content = e.target.value"></textarea>
        <button class = "send-button" >Enviar</button>
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
.send-button{
    background-color:blue;
}
</style>
