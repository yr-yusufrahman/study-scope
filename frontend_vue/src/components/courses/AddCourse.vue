<script setup>
import { defineProps, ref } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'

// State
const store = useCourseStore()
const new_title = ref('')

function handleAdd() {
    if (store.addCourse(new_title.value)) {
        new_title.value = ''    
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
