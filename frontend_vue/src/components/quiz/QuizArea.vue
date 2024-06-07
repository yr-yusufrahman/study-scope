<script setup>
import { ref, onBeforeMount, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import MultipleChoice from './MultipleChoice.vue'
import RevealAnswer from './RevealAnswer.vue'

import { useCardStore } from '@/stores/CardStore'
import { useQuizStore } from '@/stores/QuizStore'

const router = useRouter()

const card_store = useCardStore()
const quiz_store = useQuizStore()

const start_flag = ref(true)
const end_flag = ref(false)
const progress = ref(0)

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


// Go to a different question
function navigate(new_location) {
    // Check if the location is the last question
    if (new_location >= quiz_store.getQuiz.length-1) {
        end_flag.value = true
    } else {
        if (end_flag.value) {
            end_flag.value = false
        }
    }

    // Check if the location is the first question
    if (new_location <= 0) {
        start_flag.value = true
    } else {
        if (start_flag.value) {
            start_flag.value = false
        }
    }
    
    // Toggle reveal answer for card type questions
    if (quiz_store.getReveal) {
        quiz_store.setReveal(false)
    }

    quiz_store.setLocation(new_location)
    quiz_store.clearOptions()
}


// End the quiz
function end() {
    quiz_store.endQuiz()
    router.push('/workspace')
}
</script>


<template>
    <div v-show="quiz_store.getLoading" class="h-full w-full flex flex-col items-center p-16">
        <h1>Loading...</h1>
    </div>

    <div v-show="!quiz_store.getLoading" class="h-full w-full flex flex-col items-center p-16">
        <!-- Progress bar, mistake counter -->
         <div class="w-full flex flex-row justify-around">
            <h1 class="pastel-red">Mistakes: {{ quiz_store.getMistakes }}</h1>
            <progress 
                class="progress progress-info w-1/2 h-2" 
                :value="quiz_store.getMarks"
                :max="quiz_store.getTotal" 
            ></progress>
            <h1 class="green">Progress: {{ quiz_store.getMarks }} Out of: {{ quiz_store.getTotal }}</h1>   
         </div>
        

        <div class="h-2/5 content-center font-semibold text-xl">
            <h1>{{ quiz_store.getQuestion }}</h1>    
        </div>

        <!-- Question/answer area -->
        <div class="w-full h-full">
            <MultipleChoice v-show="quiz_store.isMultipleChoice" />
            <RevealAnswer v-show="!quiz_store.isMultipleChoice" />
        </div>

        <!-- Navigation buttons -->
        <div class="divider pt-8"></div>
        <div class=" w-4/5 flex flex-row justify-between">
            <button @click="navigate(quiz_store.getLocation-1)" :disabled="start_flag" class="btn btn-primary">Back</button>
            <button 
                v-show="end_flag && (quiz_store.getMarks === quiz_store.getTotal)" 
                @click="end"
                class="btn btn-ghost" 
            >Done</button>

            <p v-show="end_flag && (quiz_store.getMarks !== quiz_store.getTotal)">All questions have not been answered</p>
            <button @click="navigate(quiz_store.getLocation+1)" :disabled="end_flag" class="btn btn-accent">Next</button>
        </div>
    </div>

</template>


<style scoped>
.green {
    color: #5ECAAE;
}

</style>