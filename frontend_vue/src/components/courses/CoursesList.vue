<script setup>
import CourseCard from './CourseCard.vue'
import AddCourse from './AddCourse.vue'

import { useRouter } from 'vue-router'
import { ref, onBeforeMount, onMounted } from 'vue'
import axios from 'axios'
import refresh from '../helpers/refresh.js'
import { useCourseStore } from '../../stores/CourseStore.js'

const router = useRouter()

// State
const store = useCourseStore()
const add = ref(false)

// Check for logged in
const token = localStorage.getItem('token')
if (token) {
    allCourses()
} else {
    router.push('/login')
}


// Get all courses for user
function allCourses() {
    const headers = {"Authorization": `Bearer ${token}`}

    axios.get('http://127.0.0.1:8000/courses/get', { headers })
    .then(response => {
        store.setCourses(response.data?.courses)
        console.log(response.data?.courses)
    })
    .catch(error => {
        refresh(router)
    })
}
// END allCourses


function saveChanges() {
    const additions = store.additions
    const edits = store.edits
    const removals = store.removals

    // If changes were made
    if (additions.length > 0 || edits.length > 0 || removals.length > 0) {
        const headers = {"Authorization": `Bearer ${token}`}
        const body = { 
            add: store.additions,
            edit: store.edits,
            remove: store.removals 
        }

        axios.post('http://127.0.0.1:8000/courses/change', body, { headers })
        .then(response => {
            console.log(response.data)
        })
        .catch(error => {
            refresh(router)
        })
    }
}
</script>


<template>
    <div class="page-layout">
        <div class="course-list">
            <CourseCard v-for="course in store.courses" 
            :id="course.id" 
            :title="course.title" />
            <AddCourse v-show="add" />    
        </div>
        <button class="btn btn-primary" @click="add = !add">Add Course</button>
        <button class="btn btn-accent" @click="saveChanges">Save Changes</button>       
    </div>
</template>


<style scoped>
.course-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
}

.page-layout {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
}
</style>