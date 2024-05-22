<script setup>
import { onMounted, ref } from 'vue'
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
//const addIndex = -1


onMounted(() => {
  if (!card_store.getChapter) {
    router.push('/workspace')
  }
})


function back() {
  router.push('/workspace')

}

// Opens input for adding new card
function toggleEdit(addIndex) {
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
      <EditCard v-for="(card, index) in card_store.getCards"
        :id="card.id" 
        :question="card.question" 
        :answer="card.answer"
        :order="card.order"
        :add-index="index"
        class=" w-full"
      />

      <div class="h-7"></div>

      <Transition>
        <div class="w-full" v-show="edit_store.isEdit(card_store.getCards.length-1)">
          <AddCard class="w-full" :add-index="card_store.getCards.length-1" />
          
          <div class="h-7"></div>
        </div>
      </Transition>

      

      <button 
        v-show="card_store.getChapter"
        class="btn btn-info"
        @click="toggleEdit(card_store.getCards.length-1)"
      >Add Card</button>
    </div>
  </div>
</template>


<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>