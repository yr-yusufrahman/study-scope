<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import Flashcard from '../workspace/Flashcard.vue'
import EditCard from './EditCard.vue'
import AddCard from './AddCard.vue'
import { useCardStore } from '@/stores/CardStore.js'
import { useToggleEditStore } from '@/stores/ToggleEditStore.js'


const router = useRouter()

const card_store = useCardStore()
const edit_store = useToggleEditStore()
const addId = -1


onMounted(() => {
  if (!card_store.currentChapter) {
    router.push('/workspace')
  }
})


function back() {
  router.push('/workspace')

}

// Opens input for adding new card
function toggleEdit() {
  edit_store.setEdit(addId)
}
</script>


<template>
  <div class="p-5 flex flex-col justify-center items-center">
    <div class=" w-full">
      <button class="btn btn-ghost" @click="back">Back</button>
    </div>

    <div class="card-list items-center card-width">
      <EditCard v-for="card in card_store.currentCards"
        :id="card.id" 
        :question="card.question" 
        :answer="card.answer"
        :order="card.order"
        class=" w-full" 
      />

      <AddCard class="w-full" v-show="edit_store.isEdit(addId)" />
      <button v-show="card_store.currentChapter" class="btn btn-info" @click="toggleEdit(addId)">Add Card</button>
    </div>
    
  </div>
</template>