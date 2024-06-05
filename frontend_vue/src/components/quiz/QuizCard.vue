<script setup>
import { ref, onBeforeMount, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCardStore } from '@/stores/CardStore.js'

const router = useRouter()

const card_store = useCardStore()

const location = ref(0)
const reveal = ref(false)
const boundary = ref(false)


function toggle() {
    reveal.value = !reveal.value
}


function navigate(new_location) {
    if (new_location >= card_store.getCards.length-1) {
        boundary.value = true
    } else {
        if (boundary.value) {
            boundary.value = false
        }
    }
    location.value = new_location       
    reveal.value = false  
}


function end() {
    router.push('/workspace')
}
</script>


<template>
    <div class="h-full w-full flex flex-col items-center justify-center ">
        
        <div class="h-2/5 content-center font-semibold text-xl">
            <h1>{{ card_store.getCards[location]?.question }}</h1>    
        </div>
        

        <div class="h-full w-3/5 shadow-xl border-4 rounded-lg flex flex-col items-center justify-center p-6">
            <p v-show="reveal">{{ card_store.getCards[location]?.answer }}</p>
            <button v-show="!reveal" @click="toggle" class="btn btn-ghost">Reveal</button>
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