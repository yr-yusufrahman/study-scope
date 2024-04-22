<script setup>
import { defineProps } from 'vue'

defineProps({
  title: String
})
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
        <button class="btn btn-primary">Delete</button>
      </div>
    </div>
  </div>
</template>
