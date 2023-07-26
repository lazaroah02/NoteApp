<script>
import { useRouter } from 'vue-router';
import { formatDate } from '@/utils/formatDate';

export default {
    setup() {
        const router = useRouter()
        return {router}
    },
    props:{
        note:Object,
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
        }
    }
}
</script>

<template>
    <div class = "card" @click="router.push(`note/${note.node.id}`)">
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