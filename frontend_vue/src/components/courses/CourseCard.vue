<script setup>
import { useRouter } from 'vue-router';
import { ref, nextTick } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '@/stores/ChapterStore';
import { useCardStore } from '@/stores/CardStore';
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import autoResize from '../helpers/textResize'

import ConfirmModal from '../helpers/ConfirmModal.vue'


const props = defineProps({
  id: Number,
  title: String,
})

const router = useRouter()
const course_store = useCourseStore()
const chapter_store = useChapterStore()
const card_store = useCardStore()
const edit_store = useToggleEditStore()
const input = ref('')


// Selects course for workspace
function selectCourse() {
  const id = props.id
  const current = Number(localStorage.getItem('selectedCourse'))

  if (current !== id) {
    card_store.clear()
    chapter_store.selectCourse(id)

  }
  router.push('/workspace')
}


// Opens input for editing course title
function toggleEdit(id) {
  edit_store.setEdit(id)

  // Focus on input after DOM renders
  nextTick(() => {
    input.value.focus()
  })
}


// Handles editing course title
function handleEdit(id, original_title) {
  id = Number(id)
  const text_area = input.value
  const new_title = text_area.value

  if (new_title !== original_title) {
    course_store.editCourse(id, new_title)
  }
  edit_store.setEdit(id)
}


// Deletes course
function handleDelete(id) {
  course_store.removeCourse(id)
}

// Opens the delete modal
function handleDeleteModal(id) {
  edit_store.setDeleteModal(0, id) // 0 for course
  //course_store.setDeleting(id)
}


</script>


<template>
  <div class="card w-96 bg-base-100 shadow-xl">
    <div class="card-body">
      
      <h2 v-show="!edit_store.isEdit(id)"  class="card-title break-all">
        <button @click="selectCourse()">{{ title }}</button>
      </h2>
      
      <form v-show="edit_store.isEdit(id)" @submit.prevent="(event) => handleEdit(id, title)">
        <textarea 
          rows="1"
          ref="input" 
          :value=title
          type="text" 
          placeholder="Title" 
          class="textarea textarea-bordered card-edit overflow-y-hidden" 
          required
          @input="autoResize($event.target)"
          @keydown.enter.prevent="handleEdit(id, title)"
        ></textarea> 
      </form>

      <p>8 Chapters</p>
      <p>Due Today!</p>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="toggleEdit(id)">Edit</button>
      </div>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="handleDelete(id)">Delete</button>

        <!-- The button to open modal -->
        <label for="delete_modal" class="btn btn-error" @click="handleDeleteModal(id)">Delete</label>

      </div>
    </div>
  </div>
</template>
