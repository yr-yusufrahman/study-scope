<script setup>
import { onMounted, watch, ref } from 'vue'
import { useCardStore } from '@/stores/CardStore.js'
import refresh from '../helpers/refresh.js'

const card_store = useCardStore();
const cards = ref([])

// Watches for changes in selected chapter
watch(() => card_store.chapter, (value) => {
    console.log('selectedChapter:', value);

    const getCards = async () => {
        const success = await card_store.getCards();
        if (!success) {
            const refreshed = await refresh()
            if (refreshed) {
                card_store.getCards()
            } else {
                router.push('/login')
            }
        } else {
            cards.value = success
        }
    }   
    getCards();
})


function chapterInCourse(chapterId) {} 
</script>


<template>
    <h1>Flashcards should be here:</h1>
    <div v-for="card in cards">
        <h1>{{ card.question }}</h1>
        <h1>{{ card.answer }}</h1>
        <h1>{{ card.order }}</h1>
        <h1>{{ card.id }}</h1>
    </div>
</template>


<style scoped>
</style>