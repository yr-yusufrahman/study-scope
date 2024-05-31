<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
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


// Changes the order of the cards in state when dropped in the droppable area
function onDrop(event) {
  card_store.setDroppedCorrectly(true)
  const update = card_store.setMoveCard()

  if (update) {
    // Forces DOM to update list of cards
    card_store.setDropUpdate()
  }
  
  stopAutoScroll()
}


// Adds card template when dragging over
function onDragOver(event) {
  let new_index = 0
  let draggable = list.value.querySelector('.dragging')

  // Find the card being dragged and its index 
  list.value.querySelectorAll('[name="card"]').forEach((card, index) => {
    if (card.classList.contains('dragging')) {
      new_index = index
    }
  })

  // Get the element after the dragged card
  const afterElement = getDragAfterItem(event.clientY).element

  // If there is no element add it to the end - this is causing problems, adding to the end of the list
  if (!afterElement) {
    list.value.appendChild(draggable)
  } else {
    list.value.insertBefore(draggable, afterElement)
  }

  card_store.setDragIndex(new_index)

  scroll(event)
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
  }, { offset: Number.NEGATIVE_INFINITY })
  
}


// Auto scroll when dragging up or down
function scroll(event) {
  const scrollSpeed = 18
  const threshold = 100

  // Event.clientY is the position of the mouse pointer relative to the top of the viewport
  if (event.clientY < threshold) {
    startAutoScroll(-scrollSpeed)
  } else if (event.clientY > window.innerHeight - threshold) {
    startAutoScroll(scrollSpeed)
  } else {
    stopAutoScroll()
  }
}

function startAutoScroll(speed) {
  
  if (card_store.getScrolling) {
    return
  }

  card_store.setScrolling(true)

  const scrollStep = () => {
    if (!card_store.getScrolling) {
      return
    }
    window.scrollBy(0, speed)
    requestAnimationFrame(scrollStep)
  }

  requestAnimationFrame(scrollStep)
  
}

function stopAutoScroll() {
  card_store.setScrolling(false)
}

</script>


<template>
  <div 
    class="p-5 flex flex-col justify-center items-center"
    @drop="onDrop"
    @dragover.prevent="onDragOver"
    @dragenter.prevent
    @dragleave.prevent="onDragLeave"
  >
    <div class=" w-full pb-1 flex flex-row">
      <button class="btn btn-ghost" @click="back">Back</button>
      <div class="w-full"></div>
      <button class="btn btn-success">Save</button>
    </div>

    <div class="card-list gap-0 items-center card-width">

      <!-- add-index is add under the card -->
      <div class=" w-full" ref="list" :key="card_store.getUpdate"> 

        <TransitionGroup name="display">
          <EditCard v-for="(card, index) in card_store.getCards"
            :key="card.id"
            :id="card.id" 
            :question="card.question" 
            :answer="card.answer"
            :order="card.order"
            :add-index="index"
            class=" w-full"
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