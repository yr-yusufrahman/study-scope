<script setup>
import ChapterCard from './ChapterCard.vue'

import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { ref, onUnmounted, onMounted, onBeforeMount } from 'vue'
import { useCourseStore } from '@/stores/CourseStore'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useDragStore } from '@/stores/DragStore'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import logout from '../helpers/logout.js'


const router = useRouter()

const course_store = useCourseStore()
const chapter_store = useChapterStore()
const drag_store = useDragStore()

const list = ref(null)
const move_course = ref(null)


onUnmounted(() => {
    drag_store.clear()
})


// Find courses for moving chapters
function findCourses() {
    if (course_store.getCourses.length === 0) {
        const request = course_store.getCoursesRequest()
        request.then((success) => {
            if (!success) {
                logout()
                router.push('/login')
            }
        })
    }
}

// Move chapter to another course
function handleMove() {
    let checked = []
    const selected_course = Number(move_course.value.value)

    // If the course is the same, do nothing
    if (selected_course !== chapter_store.getCourse && selected_course) {
        list.value.querySelectorAll('input[type="checkbox"]:checked').forEach((checkbox) => {
            let id = Number(checkbox.value) 
            if (!checked.includes(id)) {
                checked.push(id)    
            }
            
        })
        chapter_store.changeChapterCourse(checked, selected_course)
        list.value.reset()
    }
}



// ----- Dragging functions -----
// Changes the order of the cards in state when dropped in the droppable area
function onDrop(event) {
  drag_store.setDroppedCorrectly(true)
  const update = drag_store.setMoveChapter()

  if (update) {
    // Forces DOM to update list of cards
    drag_store.setDropUpdate()
  }
  
  stopAutoScroll()
}


// Adds card template when dragging over a certain position
function onDragOver(event) {
  let new_index = 0

  // Get the card being dragged
  let draggable = list.value.querySelector('.dragging')

  // Find the card being dragged and its index 
  list.value.querySelectorAll('[name="modal-chapter"]').forEach((card, index) => {
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

  drag_store.setDragIndex(new_index)
  dragScroll(event)
}


// Get the closest element to the dragged card
function getDragAfterItem(y) {
  const draggableElements = [...list.value.querySelectorAll('[name="modal-chapter"]:not(.dragging)')]
  
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
function dragScroll(event) {
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
  if (drag_store.getScrolling) {
    return
  }

  drag_store.setScrolling(true)

  const scrollStep = () => {
    if (!drag_store.getScrolling) {
      return
    }
    window.scrollBy(0, speed)
    requestAnimationFrame(scrollStep)
  }

  requestAnimationFrame(scrollStep)
  
}

function stopAutoScroll() {
  drag_store.setScrolling(false)
}

</script>

<!-- Used to delete and move chapters in the directory -->
<template>
  <!-- The button to open modal -->
  <label for="move_modal" class="btn btn-info">Options</label>

  <!-- Put this part before </body> tag -->
  <input type="checkbox" id="move_modal" class="modal-toggle" />
  <div class="modal" role="dialog">
    <div 
      class="modal-box"
      @drop="onDrop"
      @dragover.prevent="onDragOver"
      @dragenter.prevent
      @dragleave.prevent
    >
      <h3 class="text-lg font-bold">Delete & Move</h3>
      <p class="py-4">
        Chapter list should be displayed here and each chapter should be draggable. Delete button is here too.
        Maybe create dividers here.
      </p>
      
      <div class=" flex flex-row items-center gap-5 pb-4">
        <select class="select select-info max-w-xs" @click="findCourses" ref="move_course">
          <option value="0" disabled selected>Select course</option>
          
          <option v-for="course in course_store.getCourses" :value="course.id">
            {{ course.title }}
          </option>
        </select>
        <button class="btn btn-accent" @click="handleMove">Move to another course</button>
      </div>

      <form id="modal-chapters" ref="list" :key="drag_store.getUpdate" @submit.prevent>
        <ChapterCard 
          v-for="(chapter, index) in chapter_store.getChapters" 
          :id="chapter.id" 
          :title="chapter.title"
          :due="chapter.next_due"
          :key="index"
          :drag="true"
        />
      </form>
    </div>

    <label class="modal-backdrop" for="move_modal">Close</label>
  </div>
</template>


<style scoped>
#modal-chapters {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding-right: 0.25rem;
    overflow-y: auto;
}
</style>
