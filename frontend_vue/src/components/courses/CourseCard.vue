<script setup>
import { defineProps, ref, nextTick } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

defineProps({
  id: Number,
  title: String,
})

const store = useCourseStore()
const edit_store = useToggleEditStore()
const input = ref('')

function toggleEdit(id) {
  edit_store.setEditCourse(id)

  // Focus on input after DOM renders
  nextTick(() => {
    input.value.focus()
  })
}

function handleEdit(e, id, original_title) {
  id = Number(id)
  const new_title = e.target[0].value
  if (new_title !== original_title && !store.courseExists(new_title)) {
    store.editCourse(id, new_title)
  } else {
    console.log('Course already exists with this name')
  }
  edit_store.setEditCourse(id)
}

function handleDelete(e) {
  const id = Number(e.target.value)
  store.removeCourse(id)
}

</script>


<template>
  <div class="card w-96 bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 v-show="!edit_store.isEditCourse(id)" class="card-title">{{ title }}</h2>
      
      <form v-show="edit_store.isEditCourse(id)" @submit.prevent="(event) => handleEdit(event, id, title)">
        <input ref="input" :value=title type="text" placeholder="Title" class="input input-bordered" />  
      </form>

      <p>8 Chapters</p>
      <p>Due Today!</p>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="toggleEdit(id)">Edit</button>
      </div>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="handleDelete" :value=id>Delete</button>
      </div>
    </div>
  </div>
</template>
