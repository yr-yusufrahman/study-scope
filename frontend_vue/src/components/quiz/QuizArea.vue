<script setup>
import { ref, onBeforeMount, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import QuizCard from './QuizCard.vue'
import { useCardStore } from '@/stores/CardStore'
import { useQuizStore } from '@/stores/QuizStore'

const router = useRouter()

const card_store = useCardStore()
const quiz_store = useQuizStore()

onBeforeMount(() => {
    const chapter = card_store.getChapter
    if (!chapter) {
        router.push('/workspace')
    } 
})

onMounted(() => {
    let request = quiz_store.getQuizRequest()
    if (!request) {
        router.push('/login')
    }
})
</script>


<template>
    <div v-show="!quiz_store.getLoading" class="h-full w-full flex flex-col items-center p-16">
        <!-- Progress bar, mistake counter -->
        <h1 class="green">Mistake counter, progress bar</h1>

        <!-- Question/answer area -->
        <div class="w-full h-full">
            <QuizCard />
        </div>
    </div>
    <div v-show="quiz_store.getLoading">
        <h1>Loading...</h1>
    </div>
</template>


<style scoped>
.green {
    color: #5ECAAE;
}
</style>