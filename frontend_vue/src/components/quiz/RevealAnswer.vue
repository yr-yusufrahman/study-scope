<script setup>
import { ref, onBeforeUpdate, onMounted, onUpdated } from 'vue'
import { useQuizStore } from '@/stores/QuizStore'

const quiz_store = useQuizStore()

const answered = ref(false)
const rating = ref(-1)

onBeforeUpdate(() => {
    if (quiz_store.isAnswered) {
        if (quiz_store.isAnswered[0] === -1) {
            answered.value = false
            rating.value = -1
        } else {
            answered.value = true
            rating.value = quiz_store.isAnswered[0]
        }
    } else {
        answered.value = false
        rating.value = -1
    }
})

function toggle() {
    quiz_store.setReveal(true)
    //answered.value = true
}


function selectRating(selected) {
    answered.value = true
    if (selected === 0) {
        quiz_store.setMistakes(quiz_store.getMistakes + 2)
        quiz_store.recordRateAnswer(0)
        rating.value = 0
    } else if (selected === 1) {
        quiz_store.setMistakes(quiz_store.getMistakes + 1)
        quiz_store.recordRateAnswer(1)
        rating.value = 1
    } else {
        quiz_store.recordRateAnswer(2)
        rating.value = 2
    }
    quiz_store.setMarks(quiz_store.getMarks + 1)
}


function matchesRating(type) {
    return type === rating.value
}
</script>


<template>
    <div class="h-full w-full flex flex-col items-center gap-6">
        <!-- Card -->
        <div 
            class="h-full w-3/5 shadow-lg border-4 rounded-lg flex flex-col items-center justify-center p-6"
        >
            <!-- Rating type -->
            <div>
                <p v-show="quiz_store.getReveal || answered" class=" text-base blue">{{ quiz_store.getAnswer }}</p>
                <button v-show="!quiz_store.getReveal && !answered" @click="toggle" class="btn btn-ghost blue">Reveal</button>             
            </div>

        </div>

        <!-- Inputs for rating -->
        <div v-show="quiz_store.getReveal || answered" class="flex flex-col items-center gap-6">
            <div class="text-base">
                <p>Could you remember the answer?</p>
            </div>

            <!-- Colour code the given rating using conditional classes -->
            <div class="w-full flex flex-row justify-center gap-6">
                <button 
                    @click="selectRating(0)" 
                    :disabled="answered" 
                    class="btn btn-ghost w-24" 
                    :class="{'red-panel': matchesRating(0)}"
                >No</button>
                <button 
                    @click="selectRating(1)" 
                    :disabled="answered" 
                    class="btn btn-ghost w-24" 
                    :class="{'amber-panel': matchesRating(1)}"
                >Almost</button>
                <button 
                    @click="selectRating(2)" 
                    :disabled="answered" 
                    class="btn btn-ghost w-24" 
                    :class="{'green-panel': matchesRating(2)}"
                >Yes</button>
            </div>                
        </div>
    </div>
</template>


<style scoped>

</style>