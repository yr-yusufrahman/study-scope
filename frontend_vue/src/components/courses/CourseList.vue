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
onMounted(() => {
    const token = localStorage.getItem('token')
    const getCourses = async () => {
        const success = await store.getCourses()
        if (!success) {
            const refreshed = await refresh()
            if (refreshed) {
                store.getCourses()
            } else {
                router.push('/login')
            }
        }
    }

    if (token) {
        getCourses()
    } else {
        router.push('/login')
    }
})


// Sends changes to backend
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
// END saveChanges
</script>


<template>
    <div class="page-layout">
        <div class="course-list">
            <CourseCard v-for="(course, index) in store.courses" 
            :id="course.id" 
            :index="index"
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