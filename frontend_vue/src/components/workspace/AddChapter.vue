<script setup>
import { defineProps, ref } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'

// State
const store = useCourseStore()
const new_title = ref('')

function handleAdd() {
    const new_chapter = new_title.value
    let success = store.addChapter(new_chapter)
    if (success) {
        new_title.value = ''
    } else {
        console.log('Failed to add chapter')
    }
}
</script>


<template>
    <form @submit.prevent="handleAdd" >
        <div class="form-control">
            <label class="label">
                <span class="label-text">Chapter name</span>
            </label>
            <input v-model="new_title" type="text" placeholder="Title" class="input input-bordered" required />
        </div>
        <div class="form-control mt-6">
            <button class="btn bg-teal-100">Add</button>
        </div>
    </form>
</template>
