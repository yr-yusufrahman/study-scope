<script setup>
import { onBeforeMount, onMounted, watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import Flashcard from './Flashcard.vue'
import { useCardStore } from '@/stores/CardStore.js'
import { useToggleEditStore } from '@/stores/ToggleEditStore.js'


const router = useRouter()

const card_store = useCardStore()
const edit_store = useToggleEditStore()

const chapter_name = ref('')
const addId = -2



// Watches for changes in selected chapter
watch(() => card_store.getChapter, (value) => {
    let request = card_store.getCardsRequest();
    if (!request) {
        router.push('/login')
    } else {
        chapter_name.value = localStorage.getItem('selectedChapterName')
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
        <h1 class=" font-bold text-center">{{ chapter_name }}</h1>
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