<script>
import { useRouter } from 'vue-router';
import { formatDate } from '@/utils/formatDate';
import {ref} from 'vue'

export default {
    setup() {
        const router = useRouter()
        const cardStyle = ref("card")
        return {router, cardStyle}
    },
    props:{
        note:Object,
        addNoteToDeletingList:Function,
        deletingNotes:Boolean,
    },
    methods:{
        validateLengthTitle(text){
            if(text.length > 20){
                return `${text.substring(0, 20)}...`
            }
            return text
        },
        validateLengthContent(text){
            if(text.length > 200){
                return `${text.substring(0, 200)}...`
            }
            return text
        },
        handleFormatDate(timeStamp){
            return formatDate(timeStamp)
        },
        addNoteToDeletingNotesList(noteId){
            this.cardStyle = "card card-red"
            this.addNoteToDeletingList(noteId)
        }
    },
    watch:{
        deletingNotes(value){
            if(!value){
                this.cardStyle = "card"
            }
        }
    },
}
</script>

<template>
    <div 
        :class = "cardStyle" 
        @click="
            deletingNotes?
                addNoteToDeletingNotesList(note.node.id)
                :
                router.push(`note/${note.node.id}`)
        "
        >
        <div class = "title">{{ validateLengthTitle(note.node.title) }}</div>
        <p class = "content">{{ validateLengthContent(note.node.content) }}</p>
        <div class = "date">{{ handleFormatDate(note.node.createdAt) }}</div>
    </div>
</template>

<style scoped>
    .card{
        padding:10px;
        padding-top:0;
        background-color: white;
        border-radius: 10px;
        cursor: pointer;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        font-family: "Cabin"!important;
    }
    .card-red{
        background-color:#ECAFAF!important;
    }
    .title{
        text-align: start;
        padding: 5px;
        font-size: 20px;
    }
    .content{
        display: flex;
        justify-content:flex-start;
        padding: 5px;
        font-size: 15px;
        height: 70%;
    }
    .date{
        text-align: end;
        width: 100%;
        font-size:12px;
    }

</style>