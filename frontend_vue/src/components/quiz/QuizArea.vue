<script setup>
import { ref, onBeforeMount, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'

// Components
import MultipleChoice from './MultipleChoice.vue'
import FillBlanks from './FillBlanks.vue'
import RevealAnswer from './RevealAnswer.vue'
import FinishModal from './FinishModal.vue'

// Stores
import { useCardStore } from '@/stores/CardStore'
import { useQuizStore } from '@/stores/QuizStore'

const router = useRouter()

const card_store = useCardStore()
const quiz_store = useQuizStore()

// State
const start_flag = ref(true)
const end_flag = ref(false)
const progress = ref(0)
const loadError = ref('')
const finished = () => quiz_store.getMarks === quiz_store.getTotal


// Check if user has a chapter selected
onBeforeMount(() => {
    const chapter = card_store.getChapter
    if (!chapter) {
        router.push('/workspace')
        return
    }

    // Check if quiz is successfully loaded
	const request = quiz_store.getQuizRequest()
	request.then((success) => {
		if (!success) {
            loadError.value = 'Could not load the quiz. Make sure the backend is running and this chapter has flashcards.'
            quiz_store.setLoading(false)
            setTimeout(() => router.push('/workspace'), 2500)
		} else {
            loadError.value = ''
            quiz_store.setLoading(false)
        }
	})
})

// Add event listener to prevent user from refreshing the page
onMounted(() => {
    // Prevent the user from leaving the quiz by refreshing the page
    window.addEventListener('beforeunload', refreshHandler)
})

// Remove event listener when the component is unmounted
onBeforeUnmount(() => {
    window.removeEventListener('beforeunload', refreshHandler)
    quiz_store.setLoading(true)
})

// Check if the user is leaving the quiz
onBeforeRouteLeave((to, from) => {
    if (!finished()) {
        const answer = window.confirm(
            'Quiz progress will be lost. Are you sure you want to leave?'
        )
        // cancel the navigation and stay on the same page
        if (!answer) return false
    }
})


// Prevent the user from refreshing the page
function refreshHandler(e) {
    e.preventDefault()
}

// Go to a different question
function navigate(new_location) {
    // Check if the location is the last question
    if (new_location >= quiz_store.getQuizLength-1) {
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


// clicking a done button which will redirect them to the workspace and save the quiz results in the revision database table
</script>


<template>
    <div v-if="loadError" class="h-full w-full flex flex-col items-center justify-center p-16">
        <p class="text-error max-w-md text-center">{{ loadError }}</p>
        <p class="mt-2 text-sm opacity-70">Returning to workspace…</p>
    </div>

    <div v-else-if="quiz_store.getLoading" class="h-full w-full flex flex-col items-center p-16">
        <button class="btn btn-ghost self-end" @click="router.push('/dashboard')">Exit</button>
        <h1>Loading...</h1>
    </div>

    <div v-else class="h-full w-full flex flex-col items-center p-16">
        <div class="w-full flex justify-end mb-2">
            <button class="btn btn-outline btn-sm" @click="router.push('/dashboard')">Exit</button>
        </div>
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
            <MultipleChoice v-show="quiz_store.getType === 0" />
            <FillBlanks v-show="quiz_store.getType === 1" />
            <RevealAnswer v-show="quiz_store.getType === 2" />
        </div>

        <!-- Navigation buttons -->
        <div class="divider pt-8"></div>
        <div class=" w-4/5 flex flex-row justify-between">
            <button @click="navigate(quiz_store.getLocation-1)" :disabled="start_flag" class="btn btn-primary">Back</button>

            <FinishModal />

            <p v-show="end_flag && (!finished())">All questions have not been answered</p>
            <button @click="navigate(quiz_store.getLocation+1)" :disabled="end_flag" class="btn btn-accent">Next</button>
        </div>
    </div>

</template>


<style scoped>
.green {
    color: #5ECAAE;
}

</style>