<script setup>
import { defineProps } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'

defineProps({
  title: String
})

const store = useCourseStore()

function handleDelete(e) {
  const title = e.target.value
  store.removeCourse(title)
}

</script>


<template>
  <div class="card w-96 bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">{{ title }}</h2>
      <p>8 Chapters</p>
      <p>Due Today!</p>
      <div class="card-actions justify-end">
        <button class="btn btn-primary">Edit</button>
      </div>
      <div class="card-actions justify-end">
        <button class="btn btn-primary" @click="handleDelete" :value=title>Delete</button>
      </div>
    </div>
  </div>
</template>
