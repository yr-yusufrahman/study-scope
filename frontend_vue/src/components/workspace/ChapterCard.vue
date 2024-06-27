<script setup>
import { ref, nextTick } from 'vue'
import { useChapterStore } from '@/stores/ChapterStore'
import { useCardStore } from '@/stores/CardStore'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import { useDragStore } from '@/stores/DragStore'
import autoResize from '../helpers/textResize'

const props = defineProps({
  id: Number,
  title: String,
  due: Object,
  drag: Boolean
})

const chapter_store = useChapterStore()
const card_store = useCardStore()
const edit_store = useToggleEditStore()
const drag_store = useDragStore()

const input = ref('')
const form = ref(null)
const dragging = ref(false)

// Selects chapter to view flashcards
function selectChapter() {
  const id = props.id
  card_store.setChapter(id)
}


// Opens input for editing chapter title
function toggleEdit(id) {
  edit_store.setEdit(id)

  // Focus on input after DOM renders
  nextTick(() => {
    input.value.focus()
  })
}


// Handles editing chapter title
function handleEdit(form_data, id, original_title) {
  const new_title = form_data[0]
  const new_chapter = new_title.value

  if (new_chapter !== original_title && new_chapter.trim() !== '') {
    chapter_store.editChapter(id, new_chapter)
  } else {
    console.log('Chapter already exists with this name or empty input.')
    new_title.value = original_title
  }

  // Close edit input
  edit_store.setEdit(id)
}

// Deletes chapter
function handleDelete(id) {
  chapter_store.removeChapter(id)
}


function handleDeleteModal(id) {
  edit_store.setDeleteModal(1, id) // 1 for chapter
}


// ----- Dragging functions -----
function dragState(state) { dragging.value = state }


// Allows dragging of cards
function startDrag(e, id) {
    dragging.value = true
    e.dataTransfer.dropEffect = 'move'
    e.dataTransfer.effectAllowed = 'move'
    // Assume dragging in undroppable area

    // Set the card being dragged
    drag_store.setDragging(id)
    drag_store.setDroppedCorrectly(false)
}


// Stops dragging of cards and correctly moves card if dropped in undroppable area
function stopDrag() {
    dragging.value = false

    // When card stops dragging, stop auto scrolling
    drag_store.setScrolling(false)

    // Check if card was dropped in undroppable area and it was moved
    if (!drag_store.getDroppedCorrectly) {

        drag_store.setDroppedCorrectly(true)

        const update = drag_store.setMoveChapter() // Force update
        
        if (update) {
            drag_store.setDropUpdate()
        }
    }

    // Stop dragging
    drag_store.setDragging(null)
}

</script>


<template>
  <div 
    class=" flex flex-row bg-base-200 rounded-lg p-1" 
    v-bind:name="drag ? 'modal-chapter' : null"
    :class="{'dragging': dragging}"
    :draggable="dragging" 
    @dragstart="startDrag($event, id)" 
    @dragend="stopDrag()"
  >
    <div class=" w-full">
      <button v-show="!edit_store.isEdit(id) && !drag" @click="selectChapter()" class="btn btn-ghost h-auto chapter-name">{{ title }}</button>

      
      <!-- Only for dragging chapter -->
      <div v-show="!edit_store.isEdit(id) && drag" class="flex flex-row items-center">
        <input type="checkbox"  class="checkbox checkbox-primary" :value="id" /> 
        <button 
          class="btn btn-ghost h-auto chapter-name"
          @mousedown="dragState(true)" 
          @mouseup="dragState(false)"
        >{{ title }}</button>
        <!-- END dragging chapter -->
      </div> 

      <form ref="form" v-show="edit_store.isEdit(id)" @submit.prevent="handleEdit(form, id, title)">
        <textarea 
          rows="1"
          ref="input" 
          :value=title
          type="text" 
          placeholder="Title" 
          class="textarea textarea-bordered card-edit overflow-y-hidden" 
          required
          @input="autoResize($event.target)"
          @keydown.enter.prevent="handleEdit(form, id, title)"
        ></textarea>
      </form>
    </div>  

    <!-- Dropdown menu -->
    <div class="relative dropdown dropdown-hover">
      <div tabindex="0" role="button" class="btn" >...</div>
      <ul tabindex="0" class="absolute glass-light dropdown-content z-[1] menu p-2 shadow rounded-box right-0">
        <li><button @click="toggleEdit(id)">Edit</button></li>
        <!--  
        <li><button @click="handleDelete(id)">Delete old</button></li>-->
        <label for="delete_modal" class="btn btn-error" @click="handleDeleteModal(id)">Delete</label>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.chapter-name {
  font-weight: bold;
  word-break: break-word;
}
</style>