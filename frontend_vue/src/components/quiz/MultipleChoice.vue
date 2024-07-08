<script setup>
import { ref, onBeforeUpdate } from 'vue'
import { useQuizStore } from '@/stores/QuizStore'


const quiz_store = useQuizStore()

const blanked_answer = ref([])
const selected_options = ref([false, false, false, false]) // Disable option buttons that have been selected
const reload = ref(0)

onBeforeUpdate(() => {
    if (quiz_store.getType === 0) {
        blanked_answer.value = splitTextIntoParts()
        reload.value = quiz_store.getHistory.length
    }
})


// Split the answer into parts to distinguish between blanked words and other text
function splitTextIntoParts() {
    let parts = []
    let remainingString = quiz_store.getAnswer
    let wordsToBlank = quiz_store.getBlanks

    // Examine each word to be blanked
    wordsToBlank?.forEach((word, index) => {
        const wordIndex = remainingString.indexOf(word)

        // If the word is found in the answer string
        if (wordIndex !== -1) {
            // Add the text before the word
            if (wordIndex > 0) {
                parts.push({ text: remainingString.substring(0, wordIndex), isWord: false })
            }

            // Add the blanked word
            parts.push({ text: word, isWord: true, index: index})
            remainingString = remainingString.substring(wordIndex + word.length)
        }
    })

    // Add the remaining text after the last blanked word
    if (remainingString.length > 0) {
        parts.push({ text: remainingString, isWord: false })
    }

    return parts
}


// Sets the options for the chosen blanked word
function chooseBlankWord(index) {
    quiz_store.setOptions(index)
    selected_options.value = [false, false, false, false]
}


// Select an option for answering the blanked word
function selectOption(option, index) {

    // If the option is the correct answer
    if (option === quiz_store.getBlankAnswer) {
        quiz_store.setMarks(quiz_store.getMarks + 1)
        quiz_store.recordMultipleChoiceAnswer(1)
        clearQuestion()
    } else {
        // Incorrect answer
        quiz_store.setMistakes(quiz_store.getMistakes + 1)
        selected_options.value[index] = true

        // Check if all 3 incorrect options have been chosen
        if (fullyAttempted()) {
            quiz_store.setMarks(quiz_store.getMarks + 1)
            quiz_store.recordMultipleChoiceAnswer(0)
            clearQuestion()
        }
    }
}


// If 3 options have been chosen, display the correct answer to blanked word
function fullyAttempted() {
    let count = 0
    selected_options.value.forEach((option) => {
        if (option === true) {
            count++
        }
    })
    return count === 3
}


function clearQuestion() {
    quiz_store.clearOptions()
    selected_options.value = [false, false, false, false]
}


</script>


<template>
    <div class="h-full w-full flex flex-col items-center justify-center gap-6">
        <!-- Multiple choice blanked answer -->
        <div v-show="quiz_store.getType === 0" class="w-4/5" >
            <p v-if="!quiz_store.isAnswered"></p>
            <p v-else>
                <span v-for="(part, index) in blanked_answer" :key="index">
                    <span v-if="part.isWord">

                        <!-- If blanked word is answered -->
                        <span v-if="quiz_store.isAnswered[part.index] === 1" class="blue">{{ part.text }}</span> 
                        
                        <!-- If all options were attempted -->
                        <span v-else-if="quiz_store.isAnswered[part.index] === 0" class="pastel-red">{{ part.text }}</span>

                        <button v-else 
                            @click="chooseBlankWord(part.index)" 
                            class="btn btn-ghost h-6 min-h-0 border-4"
                        >
                            <p class="blue">______</p>
                        </button>

                    </span>
                    <span v-else>{{ part.text }}</span>
                </span>
            </p>

        </div>

        <!-- Options -->
        <div class="flex flex-row gap-6" v-show="quiz_store.getOptions?.length != 0">
            <TransitionGroup name="options">
                <div v-for="(option, index) in quiz_store.getOptions" :key="index">
                    <button 
                        @click="selectOption(option, index)"
                        :disabled="selected_options[index]" 
                        class="btn btn-ghost"
                    >{{ option }}</button>
                </div>
            </TransitionGroup>
        </div>
    </div>
</template>


<style scoped>
</style>