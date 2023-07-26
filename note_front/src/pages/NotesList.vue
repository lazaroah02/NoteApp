<script>
import {ref} from 'vue'
import {getNotes, bulkDeleteNotes} from '../services/notesService'
import {useRouter} from 'vue-router'
import NoteComponent from '../components/NoteComponent.vue'
import {debounce} from '../utils/debounce'
import LoaderComponent from '../components/LoaderComponent.vue'

export default {
    name:"NotesList",
    setup() {
        const notes = ref([])
        const router = useRouter()
        const orderBy = ref("-created_at")
        const contains = ref("")
        const loading = ref(true)
        const loadingSearch = ref(false)
        const deletingNotes = ref(false)
        const notesToDelete = ref([])

        const searchWithDebounce = debounce((func) => {
            func()
        }, 500);

        return {notes, router, orderBy, contains, loading, loadingSearch, searchWithDebounce, deletingNotes, notesToDelete}
    },
    methods:{
        handleDeleteNotes(){
            let notesToDeleteCopy = [...this.notesToDelete]
            let choice = window.confirm("Are you sure you want to delete your notes")
            if(choice){
                bulkDeleteNotes({notesId:notesToDeleteCopy, token:this.userToken})
                .then(data => {
                    if(data.errors){
                        alert("Error to delete notes")
                    }
                    else{
                        this.deletingNotes = false
                        this.removeNotesFromNoteList(notesToDeleteCopy)
                    }
                })
            }
        },
        removeNotesFromNoteList(notesId){
            let notesCopy = [...this.notes]
            this.notes = notesCopy.filter(note => {
                notesId.indexOf(note.node.id) === -1
            });
        },
        fetchNotes(token){
            if(token){
                getNotes({token:token, orderBy:this.orderBy, contains:this.contains})
                    .then(data => {
                        this.notes = data.data.notes.edges
                        this.loading = false
                        this.loadingSearch = false
                    })
            }
        },
        handleFilter(){
            this.loadingSearch = true
            if(this.orderBy === "-created_at"){
                this.orderBy = "created_at"
            }
            else{
                this.orderBy = "-created_at"
            }
            this.fetchNotes(this.userToken)
        },
        handleSearch(e){
            this.loadingSearch = true
            if(e){
                e.preventDefault()
            }
            this.fetchNotes(this.userToken)
        },
        addNoteToDeletingList(noteId){
            this.notesToDelete.push(noteId)
        }
    }, 
    components:{
        NoteComponent,
        LoaderComponent,
    },
    //when user token change to fecth user notes
    computed:{
        userToken(){
            return this.$store.state.infoUser.token
        }
    },
    watch:{
        userToken(token){
            this.fetchNotes(token)
        },
        //when the user type a search, fetch the notes that match 
        contains(){
            this.searchWithDebounce(this.handleSearch)
        },
        deletingNotes(value){
            if(!value){
                this.notesToDelete = []
            }
        }
    },
    mounted(){
        this.fetchNotes(this.userToken)
    },
}
</script>

<template>
    <div class = "page-background">
        <section class = "notes-panel">
            <div class = "notes-title-container">
                <div class = "notes-title"><span>Green</span> Notes <img alt = "notes-logo" src = "../assets//logo.png"/></div>
                <div class = "notes-welcome-message">Hi {{ $store.state.infoUser.username }}, here are your notes</div>
            </div>
            <form class = "search-form" @submit="(e) => handleSearch(e)">
                <div class = "search-icon"><img alt = "search-icon" src = "../assets/search-icon.svg"/></div>
                <input 
                    type = "text" 
                    placeholder = "Search for words ..." 
                    v-model="contains" 
                    />
                <div v-if="loadingSearch" class = "loader-container"><LoaderComponent/></div>   
                <button type = "button" class = "order-by-button" @click="handleFilter()">
                    <img alt = "filter-icon" src = "../assets/filter-icon.svg"/>
                    <span>{{ orderBy === "-created_at"?'Recent':'Old' }}</span>
                </button>
            </form>
            <div class = "notes-loader" v-if="loading"><div><LoaderComponent/></div></div>
            <div class = "not-notes-message" v-if="notes.length === 0">There is not Notes</div>
            <div class = "cards-container">
                <NoteComponent 
                    v-for="note in notes"  
                    :key="note.node.id" 
                    :note = "note" 
                    :addNoteToDeletingList = "addNoteToDeletingList"
                    :deletingNotes = "deletingNotes"
                    />
            </div>
        </section>
        <div class = "select-notes-to-delete-message" v-if="deletingNotes && notesToDelete.length === 0">Select notes to delete</div>
        <button 
            class = "confirm-notes-deletion"
            v-if="deletingNotes && notesToDelete.length>0"
            @click="handleDeleteNotes()"
            ><img alt = "trash" src = "../assets/trash.svg"/></button>
        <button 
            v-if="notes.length > 0" 
            :class = "deletingNotes?'delete-notes-button cancel-deletion':'delete-notes-button'"
            @click="deletingNotes = !deletingNotes"
            ><img v-if = "deletingNotes" alt = 'x' src = "../assets/x-icon.svg"/>{{ !deletingNotes?'-':null }}</button>
        <button class = "create-note-button" @click="router.push(to = '/notes/add')">+</button>
    </div>
</template>

<style scoped>
    .notes-panel{
        height: 100vh;
        width: 96%;
        position: absolute;
        background-color: #fff8e4f0;
        border-top-right-radius: 250px;
        display: flex;
        flex-direction: column;
        font-family: "Raleway";
        padding-left: 20px;
    }
    .notes-title-container{
        width: 80%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    .notes-title{
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        font-size: 30px;
    }
    .notes-title span{
        color:green;
        margin-right: 10px;
        font-weight: bold;
        background-image: linear-gradient(to right, #477456, #88BE99);
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .notes-title img{
        width: 30px;
        height: 30px;
        margin-top:5px
    }
    .notes-welcome-message{
        margin-top:10px;
    }
    .search-form{
       display:flex;
       flex-direction: row;
       justify-content: flex-start;
    }
    .search-icon{
        background-color: white;
        display:flex;
        align-items: center;
        padding: 5px;
        border-bottom-left-radius: 10px;
        border-top-left-radius: 10px;
    }
    .loader-container{
       width: 20px;
       height: 20px;
       position: absolute;
       left:380px;
       padding-top:3px;
    }
    .notes-loader{
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        position: absolute;
        top:50vh
    }
    .notes-loader div{
        width: 36px;
        height: 36px;
    }
    .search-form input{
        width: 350px;
        border: 0;
        border-bottom-right-radius: 10px;
        border-top-right-radius: 10px;
        padding-right: 10px;
    }
    .search-form input:focus{
        outline: none;
    }   
    .order-by-button{
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
        margin-left: 10px;
        border: 0;
        border-radius: 10px;
        background-color: #F3F1E7;
        cursor: pointer;
    }
    .order-by-button img{
        width: 20px;
    }
    .create-note-button{
        position: fixed;
        bottom: 50px;
        right: 50px;
        width: 45px;
        height: 45px;
        border-radius: 100%;
        font-size: 30px;
        background-color: #5CAF79;
        color:white;
        border:0;
        cursor: pointer;
    }
    .delete-notes-button{
        background-color: #DC6161;
        width: 40px;
        height: 40px;
        position:fixed;
        bottom: 120px;
        right: 53px;
        color:white;
        border-radius: 100%;
        border:0;
        cursor:pointer;
        font-size: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .cancel-deletion{
        background-color:blue!important;
        padding-top: 8px;
    }
    .confirm-notes-deletion{
        background-color: red;
        width: 40px;
        height: 40px;
        position:fixed;
        bottom: 180px;
        right: 53px;
        color:white;
        border-radius: 100%;
        border:0;
        cursor:pointer;
    }
    .select-notes-to-delete-message{
        width: 200px;
        background-color:#DC6161;
        margin:0 auto;
        position:relative;
        right: 20px;
        top:90vh;
        color:white;
        text-align:center;
        border-radius: 10px;
        height: 30px;
        font-family: 'Raleway';
        padding-top: 10px;
    }
    .not-notes-message{
        width: 96%;
        text-align: center;
        position:relative;
        top:40vh;
        color:red
    }
    .cards-container{
        display: grid;
        width: 90vw;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap:30px;
        margin-top:20px;
        padding-right: 20px;
        max-height: 80vh;
        overflow-y: auto;
        scroll-snap-type: y mandatory;
        padding-bottom: 200px;
    }
    .cards-container::-webkit-scrollbar{ 
        background-color: transparent;
        width: 10px;
    }
    .cards-container::-webkit-scrollbar-thumb {
        background-color: #707070; 
        border-radius: 20px;
        border: 3px solid #f5f5f5;
    }

    /*Mobile*/
    @media (max-width:600px) {
        .notes-panel{
            border-top-right-radius: 0px;
        }
        .cards-container{
            width: 90vw;
            grid-template-columns: repeat(auto-fit, minmax(200px, 95%));
            margin: 0 auto;
            margin-top:20px;
        }
        .cards-container::-webkit-scrollbar{ 
            display: none;
        }
        .search-form input{
            width: 200px;
        }
        .loader-container{
            left:230px;
        }
    }
</style>