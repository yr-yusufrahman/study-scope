<script setup>
import { defineProps, ref } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'

defineProps({
  id: Number,
  title: String
})

const store = useCourseStore()
const edit = ref(false)


function handleEdit(e, id, original_title) {
  id = Number(id)
  const new_title = e.target[0].value
  if (new_title !== original_title && !store.courseExists(new_title)) {
    store.editCourse(id, new_title)
    edit.value = false
  } else {
    console.log('Course already exists with this name')
  }
}

function handleDelete(e) {
  const id = Number(e.target.value)
  store.removeCourse(id)
}

</script>


<template>
  <div class="card w-96 bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 v-show="!edit" class="card-title">{{ title }}</h2>
      
      <form v-show="edit" @submit.prevent="(event) => handleEdit(event, id, title)">
        <input :value=title type="text" placeholder="Title" class="input input-bordered" />  
      </form>

      <p>8 Chapters</p>
      <p>Due Today!</p>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="edit = !edit">Edit</button>
      </div>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="handleDelete" :value=id>Delete</button>
      </div>
    </div>
  </div>
</template>
