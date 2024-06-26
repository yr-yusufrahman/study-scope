<script setup>
import { ref } from 'vue'
import { useCardStore } from '@/stores/CardStore.js'


const card_store = useCardStore()

const current = ref(0)
const show = ref(false)

function toggle() {
    show.value = !show.value
}

function navigate(forward) {
    if (forward) {
        current.value++
    } else {
        current.value--
    }
    show.value = false
}
</script>


<template>
    <section>
        <div class=" shadow-lg bg-white rounded-md min-h-20 content-center" :class="{'border-teal-300 border-4': show}">
            <button v-show="!show" class=" w-full" @click="toggle">{{ card_store.getCards[current]?.question }}</button>
            <button v-show="show" class=" w-full" @click="toggle">{{ card_store.getCards[current]?.answer }}</button>
        </div>
        <div class="flex flex-row items-center justify-center pt-4 gap-4">
            <button 
                class="btn btn-ghost" 
                :disabled="current === 0"
                @click="navigate(false)"
            >Previous</button>
            <p>{{ current }} of {{ card_store.getCards.length }}</p>
            <button 
                class="btn btn-ghost" 
                :disabled="current === card_store.getCards?.length-1"
                @click="navigate(true)"
            >Next</button>
        </div>
    </section>
</template>


