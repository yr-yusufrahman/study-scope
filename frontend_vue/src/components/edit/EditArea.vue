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
const list = ref(null)


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


// Changes the order of the cards in state when dropped
function onDrop(event, new_index) {
  const card_index = event.dataTransfer.getData('cardIndex')
  console.log("Dropped item was at: ", card_index, ", now at: ", new_index)
  if (card_index !== new_index) {
    
    card_store.setMoveCard(card_index, new_index)
  }
}


// Adds card template when dragging over
function onDragOver(event) {
  const afterElement = getDragAfterItem(event.clientY)
  const draggable = list.value.querySelector('.dragging')

  // If there is no element after the dragged card, add it to the end
  if (afterElement == null) {
    list.value.appendChild(draggable)
  } else {
    list.value.insertBefore(draggable, afterElement)
  }
}


// Get the closest element to the dragged card
function getDragAfterItem(y) {
  const draggableElements = [...list.value.querySelectorAll('[name="card"]:not(.dragging)')]
  
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2

    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
  
}

</script>


<template>
  <div class="p-5 flex flex-col justify-center items-center">
    <div class=" w-full pb-1 flex flex-row">
      <button class="btn btn-ghost" @click="back">Back</button>
      <div class="w-full"></div>
      <button class="btn btn-success">Save</button>
    </div>

    <div class="card-list gap-0 items-center card-width"  @dragover.prevent>

      <!-- add-index is add under the card -->
      <div class=" w-full" ref="list"> 
        <TransitionGroup name="display">
          <EditCard v-for="(card, index) in card_store.getCards"
            :key="card.id"
            :id="card.id" 
            :question="card.question" 
            :answer="card.answer"
            :order="card.order"
            :add-index="index"
            class=" w-full"
            @dragenter.prevent
            @dragover.prevent="onDragOver"
            @drop="onDrop($event, index)" 
          />
        </TransitionGroup>
      </div>

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


/* Fade out after deleting */
.display-leave-active {
  transition: opacity 0.3s ease;
}

.display-leave-to {
  opacity: 0;
}
</style>