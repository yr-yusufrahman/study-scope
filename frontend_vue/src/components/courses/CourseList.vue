<script setup>
import CourseCard from './CourseCard.vue'
import AddCourse from './AddCourse.vue'
import ConfirmModal from '../helpers/ConfirmModal.vue'

import { useRouter, onBeforeRouteLeave } from 'vue-router'
import { ref, onUnmounted, onMounted, onBeforeMount } from 'vue'
import logout from '../helpers/logout.js'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

const router = useRouter()

// State
const course_store = useCourseStore()
const edit_store = useToggleEditStore()
const addId = -1
const loading = ref(true)
const loadError = ref(false)


// Check for logged in
onBeforeMount(() => {
	const request = course_store.getCoursesRequest()
	request.then((success) => {
		loading.value = false
		if (!success) {
			loadError.value = true
			logout()
			router.push('/login')
			return
		}
		loadError.value = false
	})
})


// Autosave changes when leaving the page
onBeforeRouteLeave((to, from) => {
  if (course_store.isModified) {
    course_store.saveCoursesRequest()
  }
})


// When leaving page
onUnmounted(() => {
    edit_store.clear()
})


// Opens input for adding new course
function toggleEdit() {
  edit_store.setEdit(addId)
}


// Sends changes to backend
function saveChanges() {
	const request = course_store.saveCoursesRequest()
	request.then((success) => {
		if (!success) {
			logout()
			router.push('/login')
		}
	})
}
// END saveChanges

</script>


<template>
    <div class="page-layout">
        <p v-if="loading" class="text-center text-lg">Loading your courses…</p>
        <p v-else-if="loadError" class="text-center text-lg">Could not load courses. Redirecting to sign in…</p>
        <p v-else-if="course_store.getCourses.length === 0" class="text-center text-lg">No courses yet — add one below.</p>
        <div class="course-list">
            <CourseCard v-for="(course, index) in course_store.getCourses" 
            :id="course.id" 
            :title="course.title"
            :key="index" />
            <AddCourse v-show="edit_store.isEdit(addId)" />
        </div>
        <button class="btn btn-info" @click="toggleEdit(addId)">Add Course</button>
        <button class="btn btn-accent" @click="saveChanges">Save Changes</button>

        <ConfirmModal :remove="true" />
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