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
        store.courses = response.data?.courses
        console.log(response.data?.courses)
    })
    .catch(error => {
        refresh(router)
    })
}
// END allCourses


</script>


<template>
    <div class="page-layout">
        <div class="course-list">
            <CourseCard v-for="course in store.courses" :id="course.id" :title="course.title"  />
            <AddCourse />    
        </div>
        <button class="btn btn-primary">Add Course</button>
        <button class="btn btn-accent">Save Changes</button>       
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