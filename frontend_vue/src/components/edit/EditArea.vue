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
const addIndex = card_store.currentCards?.length - 1


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
  edit_store.setEdit(addIndex)
}
</script>


<template>
  <div class="p-5 flex flex-col justify-center items-center">
    <div class=" w-full pb-1">
      <button class="btn btn-ghost" @click="back">Back</button>
    </div>

    <div class="card-list gap-0 items-center card-width">
      <!-- last-add ensures hidden add input is not displayed in the last card. add-index is add under the card -->
      <EditCard v-for="(card, index) in card_store.currentCards"
        :id="card.id" 
        :question="card.question" 
        :answer="card.answer"
        :order="card.order"
        :last-add="index !== addIndex"
        :add-index="index"
        class=" w-full"
      />

      <div class="h-7"></div>
      <AddCard class="w-full" :add-index="addIndex" v-show="edit_store.isEdit(addIndex)" />
      <button v-show="card_store.currentChapter" class="btn btn-info" @click="toggleEdit(addIndex)">Add Card</button>
    </div>
    
  </div>
</template>