<script setup>
import { ref, onBeforeUpdate } from 'vue'
import { useQuizStore } from '@/stores/QuizStore'


const quiz_store = useQuizStore()

const blanked_answer = ref([])
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
    let remaining_string = quiz_store.getAnswer
    let wordsToBlank = quiz_store.getBlanks

    // Examine each word to be blanked
    wordsToBlank?.forEach((word, index) => {
		const formatted_string = remaining_string.toLowerCase()
		const wordIndex = formatted_string.indexOf(word)

        // If the word is found in the answer string
        if (wordIndex !== -1) {
            // Add the text before the word
            if (wordIndex > 0) {
                parts.push({ text: remaining_string.substring(0, wordIndex), isWord: false })
            }

            // Add the blanked word
            parts.push({ text: word, isWord: true, index: index})
            remaining_string = remaining_string.substring(wordIndex + word.length)
        }
    })

    // Add the remaining text after the last blanked word
    if (remaining_string.length > 0) {
        parts.push({ text: remaining_string, isWord: false })
    }

    return parts
}


// Sets the options for the chosen blanked word
function chooseBlankWord(index) {
    quiz_store.setOptions(index)
}


// Select an option for answering the blanked word
function selectOption(option, index) {
    // If the option is the correct answer
    if (option === quiz_store.getBlankAnswer) {
        quiz_store.setMarks(quiz_store.getMarks + 1)
        //quiz_store.recordChoiceAnswer(1)
        quiz_store.recordChoiceAnswerNew(1, index)
        clearQuestion()
    } else {
        // Incorrect answer
        quiz_store.setMistakes(quiz_store.getMistakes + 1)
        quiz_store.recordChoiceAnswerNew(0, index)
        // Check if all 3 incorrect options have been chosen
        if (quiz_store.allChoicesAnsweredNew(quiz_store.getBlankIndex)) {
            quiz_store.setMarks(quiz_store.getMarks + 1)
            //quiz_store.recordChoiceAnswer(0)
            
            clearQuestion()
        }
    }
}


function clearQuestion() {
    quiz_store.clearOptions()
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
                        <span v-if="quiz_store.isCorrectChoice(part.index)" class="blue">{{ part.text }}</span> 
                        
                        <!-- If all options were attempted -->
                        <span v-else-if="quiz_store.allChoicesAnsweredNew(part.index)" class="pastel-red">{{ part.text }}</span>

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
                        :disabled="quiz_store.choiceAnswered(index)" 
                        class="btn btn-ghost"
                    >{{ option }}</button>
                </div>
            </TransitionGroup>
        </div>
    </div>
</template>


<style scoped>
</style>