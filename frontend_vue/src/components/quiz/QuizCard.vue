<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, onBeforeUpdate } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/QuizStore'
import { useCardStore } from '@/stores/CardStore.js'

const router = useRouter()

const quiz_store = useQuizStore()

const location = ref(0)
const reveal = ref(false)
const boundary = ref(false)
const blanked_answer = ref([])
const options = ref([])
const answering_index = ref(-1)


onBeforeUpdate(() => {
    if (quiz_store.getQuiz[location.value]?.multiple_choice) {
        blanked_answer.value = splitTextIntoParts(location.value)
    } else {
        resetMCQ()
    } 
})


function toggle() {
    reveal.value = !reveal.value
}


function navigate(new_location) {
    if (new_location >= quiz_store.getQuiz.length-1) {
        boundary.value = true
    } else {
        if (boundary.value) {
            boundary.value = false
        }
    }
    quiz_store.setLocation(new_location)
    quiz_store.clearOptions()
    location.value = new_location
    reveal.value = false
    resetMCQ()
}


function end() {
    router.push('/workspace')
}


// Split the answer into parts to be displayed
function splitTextIntoParts(location) {
    let parts = [];
    let remainingString = quiz_store.getAnswer
    let wordsToBlank = quiz_store.getBlanks

    wordsToBlank.forEach((word, index) => {
    const wordIndex = remainingString.indexOf(word);
    if (wordIndex !== -1) {
        if (wordIndex > 0) {
        parts.push({ text: remainingString.substring(0, wordIndex), isWord: false });
        }
        parts.push({ text: word, isWord: true, index: index});
        remainingString = remainingString.substring(wordIndex + word.length);
    }
    });

    if (remainingString.length > 0) {
    parts.push({ text: remainingString, isWord: false });
    }

    return parts;
}


// Sets the options for the chosen blanked word
function chooseBlank(index) {
    quiz_store.setOptions(index)
}


function resetMCQ() {
    blanked_answer.value = []
    options.value = []
    answering_index.value = -1

}


function selectOption(option) {
    if (option === quiz_store.getBlankAnswer) {
        console.log('Correct')
    } else {
        console.log('Incorrect')
    }
}
</script>


<template>   

    <!-- Main question area -->
    <div class="h-full w-full flex flex-col items-center gap-6">
        <!-- Card -->
        <div 
            v-show="!quiz_store.isMultipleChoice"
            class="h-full w-3/5 shadow-lg border-4 rounded-lg flex flex-col items-center justify-center p-6"
        >
            <!-- Rating type -->
            <div>
                <p v-show="reveal" class=" text-base blue">{{ quiz_store.getAnswer }}</p>
                <button v-show="!reveal" @click="toggle" class="btn btn-ghost blue">Reveal</button>             
            </div>

        </div>

        <!-- Inputs for rating -->
        <div v-show="!quiz_store.isMultipleChoice && reveal" class="flex flex-col items-center gap-6">
            <div class="text-base">
                <p>Could you remember the answer?</p>
            </div>

            <div class="w-full flex flex-row justify-center gap-6">
                <button class="btn btn-ghost w-24">No</button>
                <button class="btn btn-ghost w-24">Almost</button>
                <button class="btn btn-ghost w-24">Yes</button>
            </div>                
        </div>
    </div>


</template>


<style scoped>
.options-enter-active,
.options-leave-active {
  transition: opacity 0.3s ease;
}

.options-enter-from,
.options-leave-to {
  opacity: 0;
}

</style>