<script setup>
import Flashcard from './Flashcard.vue'
import CarouselSlide from './CarouselSlide.vue'

import { onBeforeMount, onMounted, watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCardStore } from '@/stores/CardStore.js'
import { useToggleEditStore } from '@/stores/ToggleEditStore.js'
import logout from '../helpers/logout.js'

const router = useRouter()

const card_store = useCardStore()
const edit_store = useToggleEditStore()
const empty = ref(true)


const makeRequest = () => {
    const request = card_store.getCardsRequest()
    request.then((success) => {
        if (!success) {
            logout()
            router.push('/login')
        }
    })
}


onBeforeMount(() => {
    const state_chapter = card_store.getChapter

    // If there is no chapter in state, check storage
    if (!state_chapter) {
        // Local storage is just for persisting on refresh
        const chapter = Number(localStorage.getItem('selectedChapter'))
        if (chapter) {
            card_store.setChapter(chapter)
        }  
    } else {
        empty.value = false
    }
})


// Watches for changes in selected chapter
watch(() => card_store.getChapter, (value) => {
    if (value) empty.value = false

    makeRequest()
})


// Opens input for editing card
function toggleEdit(id) {
  edit_store.setEdit(id)
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
		<h1 v-show="empty" class="text-center">Click a chapter to show flashcards!</h1>


		<section v-show="!empty" class="flex flex-col gap-10">
			<!-- Heading -->
			<div class="flex flex-row justify-around">
				<h1 v-show="card_store.getDue?.days">Next due in {{ card_store.getDue?.days }} days</h1>
				<h1 class=" font-bold text-center">{{ card_store.getChapterName }}</h1>

				<div v-show="card_store.getChapter && card_store.getCards.length != 0">

					<button 
						class="btn btn-primary"
						@click="goToQuiz"
					>Begin Quiz</button>                    
				</div>

			</div>

			<!-- Flashcards -->
			<CarouselSlide v-show="card_store.getChapter && card_store.getCards.length != 0" />

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
		</section>
	</div>
</template>


<style scoped>
#cards {
    width: 90%;
}

</style>