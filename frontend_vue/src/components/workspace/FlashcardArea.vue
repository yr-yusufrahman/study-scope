<script setup>
import { onMounted, watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import Flashcard from './Flashcard.vue'
import AddCard from './AddCard.vue'
import { useCardStore } from '@/stores/CardStore.js'
import { useToggleEditStore } from '@/stores/ToggleEditStore.js'


const router = useRouter()

const card_store = useCardStore()
const edit_store = useToggleEditStore()
const addId = -2

// When the user leaves and clicks on another course, the 

// Watches for changes in selected chapter
watch(() => card_store.currentChapter, (value) => {
    console.log('selectedChapter:', value);
    let request = card_store.getCardsRequest();
    if (!request) {
        router.push('/login')
    }
})


// Opens input for adding new card
function toggleEdit() {
  edit_store.setEdit(addId)
}


function chapterInCourse(chapterId) {} 
</script>


<template>
    <div class="overflow-y-auto p-5">
        <h1>Flashcards should be here:</h1>
        <div class="card-list">    
            <Flashcard v-for="card in card_store.currentCards" 
            :id="card.id" 
            :question="card.question" 
            :answer="card.answer"
            :order="card.order" />
            <AddCard v-show="edit_store.isEdit(addId)" />
        </div>
        <button v-show="card_store.currentChapter" class="btn btn-info" @click="toggleEdit(addId)">Add Card</button>
    </div>
</template>


<style scoped>
.card-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}
</style>