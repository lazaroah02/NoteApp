<script>
    import { defineComponent, ref } from 'vue'
    import { createNote } from '../services/notesService';
    import {useRouter} from 'vue-router'
    import './commonStyles/pages.css'
    import './commonStyles/addNote-editNote-styles.css'

    export default defineComponent({
        name:"AddNote",
        setup(){
            const title = ref("")
            const content = ref("")
            const router = useRouter()
            return {title, content, router}
        },
        methods:{
            handleCreateNote(e){
                e.preventDefault();
                createNote({data:{title:this.title, content:this.content}, token:this.$store.state.infoUser.token})
                .then((data) => {
                    if(data.errors){
                        alert("Error al crear la nota")
                    }
                    else{
                        this.router.push("/")
                    }
                })
            },
        }
    })
</script>

<template>
    <main class = "page-background">
        <div class = "panel">
            <div class = "title"><span>Green</span> Notes</div>
            <form class = "note-form" @submit="(e) => handleCreateNote(e)">
                <div class = "go-back-button-and-input-title-container">
                    <button 
                        class = "go-back-button" 
                        type = "button"
                        @click="router.push('/')"
                        ><img alt = "chevron-left" src = "../assets/chevron-left.svg"/></button>
                    <input class = "input-title" type="text" placeholder="Title" @change="e => title = e.target.value"/>
                </div>
                <textarea class = "input-content" @change="e => content = e.target.value"></textarea>
                <button @click = "router.push('/')" class = "cancel-button"><img alt = "trash" src = "../assets/trash.svg"/></button>
                <button class = "send-button"><img alt = "check" src = "../assets/check-icon.svg"/></button>
            </form>
        </div>
    </main>
</template>

<style scoped>

</style>
