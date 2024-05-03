<script setup>
import ChapterCard from './ChapterCard.vue'
import AddChapter from './AddChapter.vue'

import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { ref, onBeforeMount, onMounted } from 'vue'
import axios from 'axios'
import refresh from '../helpers/refresh.js'
import { useCourseStore } from '../../stores/CourseStore.js'

const router = useRouter()


// State
const store = useCourseStore()
const chapters = ref([]) // Get chapters from selected course
const add = ref(false)


// Check for logged in
onMounted(() => {
    const token = localStorage.getItem('token')
    const getChapters = async () => {
        const success = await store.getCourses()
        if (success) {
            chapters.value = store.selectedChapters()
        } else {
            const refreshed = await refresh()
            if (refreshed) {
                store.getCourses()
                chapters.value = store.selectedChapters()
            } else {
                router.push('/login')
            }
        }
    }

    if (token) {
        chapters.value = store.selectedChapters()
        // If no chapters, get courses again
        if (!chapters.value) {
            getChapters()
        } 
    } else {
        router.push('/login')
    }
})


// Sends changes to backend
function saveChanges() {

}
// END saveChanges
</script>


<template>
    <div id="panel" class="shadow-xl flex flex-col gap-4 overflow-y-auto">  
        <div class="text-m breadcrumbs">
            <ul>
                <li><RouterLink to="/courses">Courses</RouterLink></li> 
                <li><a>Selected course</a></li> 
            </ul>
        </div> 

        <div class="flex flex-col gap-3">
            <ChapterCard v-for="chapter in chapters" :id="chapter.id" :title="chapter.title" />
        </div>

        
        <AddChapter v-show="add" />    
        

        <div class="card">
            
            <button class="btn btn-primary" @click="add = !add">Add Chapter</button>  
            <button class="btn btn-accent" @click="saveChanges">Save Changes</button>    
        </div>
        
              
    </div>
</template>


<style scoped>
#panel {
    height: 100%;
    padding: 0.5rem;
}

</style>