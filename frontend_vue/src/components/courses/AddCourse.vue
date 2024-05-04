<script setup>
import { ref, nextTick } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

// State
const store = useCourseStore()
const edit_store = useToggleEditStore()
const addId = -1
const new_title = ref('')

// Opens input for adding new course
function toggleEdit(id) {
  edit_store.setEdit(id)

  // Focus on input after DOM renders
  nextTick(() => {
    new_title.value.focus()
  })
}


function handleAdd(e) {
    const new_title = e.target[0].value
    if (store.addCourse(new_title)) {
        new_title.value = ''    
    } else {
        console.log('Course already exists')
    }
}
</script>


<template>
    <div v-show="edit_store.isEdit(addId)" class="card w-96 bg-base-100 shadow-xl">
        <form class="card-body" @submit.prevent="handleAdd" >
            <div class="form-control">
                <label class="label">
                    <span class="label-text">Course title</span>
                </label>
                <input ref="new_title"  type="text" placeholder="Title" class="input input-bordered" required />
            </div>
            <div class="form-control mt-6">
                <button class="btn btn-accent">Add</button>
            </div>
        </form>
    </div>
    <button class="btn btn-primary" @click="toggleEdit(addId)">Add Course</button>
</template>
