<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, onBeforeUpdate } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/QuizStore'
import { useCardStore } from '@/stores/CardStore.js'

const router = useRouter()

const quiz_store = useQuizStore()
const card_store = useCardStore()

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
    let remainingString = quiz_store.getQuiz[location]?.answer
    let wordsToBlank = quiz_store.getQuiz[location]?.blanked

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
    answering_index.value = index
    let option_list = quiz_store.getQuiz[location.value]?.options[index]
    option_list.push(quiz_store.getQuiz[location.value]?.blanked[index])
    options.value = option_list
}


function resetMCQ() {
    blanked_answer.value = []
    options.value = []
    answering_index.value = -1

}
</script>


<template>
    <div class="h-full w-full flex flex-col items-center justify-center ">
        
        <div class="h-2/5 content-center font-semibold text-xl">
            <h1>{{ quiz_store.getQuiz[location]?.question }}</h1>    
        </div>
        

        <!-- Main question area -->
        <div class="h-full w-full flex flex-col items-center gap-6">
            <!-- Card -->
            <div 
                v-show="!quiz_store.getQuiz[location]?.multiple_choice"
                class="h-full w-3/5 shadow-lg border-4 rounded-lg flex flex-col items-center justify-center p-6"
            >
                <!-- Rating type -->
                <div>
                    <p v-show="reveal" class=" text-base blue">{{ quiz_store.getQuiz[location]?.answer }}</p>
                    <button v-show="!reveal" @click="toggle" class="btn btn-ghost blue">Reveal</button>             
                </div>

            </div>

            <!-- Inputs for rating -->
            <div v-show="!quiz_store.getQuiz[location]?.multiple_choice && reveal" class="flex flex-col items-center gap-6">
                <div class="text-base">
                    <p>Could you remember the answer?</p>
                </div>

                <div class="w-full flex flex-row justify-center gap-6">
                    <button class="btn btn-ghost w-24">No</button>
                    <button class="btn btn-ghost w-24">Almost</button>
                    <button class="btn btn-ghost w-24">Yes</button>
                </div>                
            </div>

            <!-- Multiple choice blanked answer -->
            <div v-show="quiz_store.getQuiz[location]?.multiple_choice">
                <p>
                    <span v-for="(part, index) in blanked_answer" :key="index">
                        <span v-if="part.isWord">
                            <button @click="chooseBlank(part.index)" class="btn btn-ghost h-6 min-h-0">
                                <p class="blue">{{ part.text }}</p>
                            </button>
                        </span>
                        <span v-else>{{ part.text }}</span>
                    </span>
                </p>

            </div>

            <!-- Options -->
            <div class="flex flex-col" v-show="options.length != 0">
                <TransitionGroup name="options">
                    <div v-for="(option, index) in options" :key="index">
                        <button class="btn btn-ghost">{{ option }}</button>
                    </div>
                </TransitionGroup>
            </div>
        </div>


        <!-- Navigation buttons -->
        <div class="divider pt-8"></div> 
        <div class=" w-4/5 flex flex-row justify-between">
            <button class="btn btn-primary" @click="navigate(location-1)" :disabled="location <= 0">Back</button>
            <button class="btn btn-ghost" v-show="boundary && reveal" @click="end">Done</button>
            <button class="btn btn-accent" @click="navigate(location+1)" :disabled="boundary">Next</button>
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