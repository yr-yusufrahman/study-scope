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
watch(() => card_store.getChapter, (value) => {
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
    if (card_store.getChapter) {
        router.push('/edit')  
    }
}

function goToQuiz() {
    if (card_store.getChapter) {
        router.push('/quiz')
    }
}
</script>


<template>
    <div id="cards" class="p-5 card-width">
        <button 
            v-show="card_store.getChapter && card_store.getCards.length != 0" 
            class="btn btn-primary"
            @click="goToQuiz"
        >Begin Quiz</button>
        <div class="card-list">
            <Flashcard v-for="card in card_store.getCards" 
            :id="card.id" 
            :question="card.question" 
            :answer="card.answer"
            :order="card.order" />
            <button 
                v-show="card_store.getChapter" 
                class="btn btn-info" 
                @click="editing"
            >Add or Remove Card</button>
        </div>
    </div>
</template>


<style scoped>
#cards {
    width: 90%;
}

</style>