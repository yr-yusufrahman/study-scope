<script setup>
import QuizCard from './QuizCard.vue'
</script>


<template>
    <div class="h-full w-full flex flex-col items-center p-16">
        <!-- Progress bar, mistake counter -->
        <h1>Mistake counter, progress bar</h1>

        <!-- Question/answer area -->
        <div class="w-full h-full">
            <QuizCard />
        </div>
    </div>
</template>