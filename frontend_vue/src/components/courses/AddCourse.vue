<script setup>
import { ref } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'

// State
const store = useCourseStore()
const new_title = ref('')

function handleAdd() {
    let new_course = { title: new_title.value }

    // Check if course already has the same title
    if (!store.courseExists(new_title.value)) {
        store.addCourse(new_course)
        console.log(new_course)        
    } else {
        console.log('Course already exists')
    }
}
</script>


<template>
    <div class="card w-96 bg-base-100 shadow-xl">
        <form class="card-body" @submit.prevent="handleAdd" >
            <div class="form-control">
                <label class="label">
                    <span class="label-text">Course title</span>
                </label>
                <input v-model="new_title" type="text" placeholder="Title" class="input input-bordered" required />
            </div>
            <div class="form-control mt-6">
                <button class="btn btn-accent">Add</button>
            </div>
        </form>
  </div>
</template>
