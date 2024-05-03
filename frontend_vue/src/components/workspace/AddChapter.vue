<script setup>
import { defineProps, ref } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'

// State
const store = useCourseStore()
const new_title = ref('')

function handleAdd() {
    let new_chapter = new_title.value
    const course_id = Number(localStorage.getItem('selectedCourse'))
    store.addChapter(course_id, new_chapter)
}
</script>


<template>
    <form class="shadow-xl" @submit.prevent="handleAdd" >
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
