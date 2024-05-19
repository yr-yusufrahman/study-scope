<script setup>
import { onMounted, watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import Flashcard from './Flashcard.vue'
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

function editing() {
    if (card_store.currentChapter) {
        router.push('/edit')  
    }
}
</script>


<template>
    <div id="cards" class="p-5 card-width">
        <h1>Flashcards should be here:</h1>
        <div class="card-list">
            <Flashcard v-for="card in card_store.currentCards" 
            :id="card.id" 
            :question="card.question" 
            :answer="card.answer"
            :order="card.order" />
            <button v-show="card_store.currentChapter" class="btn btn-info" @click="editing">Add or Remove Card</button>
        </div>
    </div>
</template>


<style scoped>
#cards {
    width: 90%;
}

</style>