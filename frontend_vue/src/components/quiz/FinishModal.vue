<script setup>
import { useRouter } from 'vue-router'

import { useQuizStore } from '@/stores/QuizStore'

const router = useRouter()
const quiz_store = useQuizStore()


// End the quiz
function end() {    
    // Save results
    let success = quiz_store.saveRevision()
    if (success) {
        router.push('/workspace')    
    }
    
}
</script>


<template>
    <!-- The button to open modal -->
    <label 
        v-show="quiz_store.getMarks === quiz_store.getTotal" 
        for="finish-modal"
        class="btn btn-info"
    >Done</label>

    <!-- Modal content -->
    <input type="checkbox" id="finish-modal" class="modal-toggle" />
    <div class="modal" role="dialog">
        <div class="modal-box">
            <h3 class="font-bold text-lg">Well Done!</h3>
            <p class="py-4">You have completed the quiz. You can now go back to the workspace.</p>
            <p class="py-4">Mistakes: {{ quiz_store.getMistakes }}, Number of answers: {{ quiz_store.getTotal }}</p>

            <!-- Modal close buttons -->
            <div class="modal-action flex flex-row justify-between">
                <label for="finish-modal" class="btn">Return</label>
                <label @click="end" for="finish-modal" class="btn btn-info">Finish</label>
            </div>
        </div>
    </div>
</template>


<style scoped>
</style>
