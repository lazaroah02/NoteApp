<script>
import {ref} from 'vue'
import {getNotes, bulkDeleteNotes} from '../services/notesService'
import {useRouter} from 'vue-router'
import {debounce} from '../utils/debounce'
import LoaderComponent from '../components/LoaderComponent.vue'
import NoteComponent from "../components/NoteComponent" 
import './commonStyles/pages.css'
import './commonStyles/notesListStyles.css'

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
        const showSearchResultStatus = ref(false)
        const searchResultStatus = ref("")

        const searchWithDebounce = debounce((func) => {
            func()
        }, 500);

        return {notes, router, orderBy, contains, loading, loadingSearch, searchWithDebounce, 
            deletingNotes, notesToDelete, showSearchResultStatus, searchResultStatus}
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
            this.notes = notesCopy.filter(note => notesId.indexOf(note.node.id) === -1);
        },
        fetchNotes(token){
            if(token){
                getNotes({token:token, orderBy:this.orderBy, contains:this.contains})
                    .then(data => {
                        this.notes = data.data.notes.edges
                        this.loading = false
                        this.loadingSearch = false
                        this.handleShowSearchStatus(data.data.notes.edges.length)
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
        handleShowSearchStatus(resultsSize){
            if(this.contains !== ""){
                this.searchResultStatus = `Found ${resultsSize} notes with word "${this.contains}"`
                this.showSearchResultStatus = true
            }else{
                this.showSearchResultStatus = false
            }
        },
        addNoteToDeletingList(noteId){
            this.notesToDelete.push(noteId)
        },
        handleLogout(){
            let choice = window.confirm("Are you sure you want to log out?")
            if(choice){
                localStorage.removeItem("jwt")
                this.$store.commit("setInfoUser", {username:null, token:null})
                this.router.push('/login')
            }
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
        <section class = "panel">
            <div class = "close-session-button" @click="handleLogout()"><img alt = "close-session" src = "../assets/turn-of-icon.svg"/></div>
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
            <div class = "search-result-status" v-if="showSearchResultStatus">{{ searchResultStatus }}</div>
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
