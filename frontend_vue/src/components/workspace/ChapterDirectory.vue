<script setup>
import EditChapterModal from './EditChapterModal.vue'
import ChapterCard from './ChapterCard.vue'
import AddChapter from './AddChapter.vue'

import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'
import refresh from '../helpers/refresh.js'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

const router = useRouter()


// State
const store = useCourseStore()
const chapter_store = useChapterStore()
const edit_store = useToggleEditStore()
const addId = -1


// Check for logged in
onMounted(() => {
    const token = localStorage.getItem('token')

    if (token) {
        let chapters = chapter_store.selectedChapters()
        const getChapters = async () => {
            const success = await store.getCourses()

            // If unsuccessful, refresh token
            if (!success) {
                const refreshed = await refresh()
                if (refreshed) {
                    store.getCourses()
                } else {
                    router.push('/login')
                }                
            }
        }
        
        // If no course was selected, go back to courses
        if (chapters === null) {
            router.push('/courses')
        } 
        // If no chapters, get courses once more and check for chapters
        else if (!chapters) {
            getChapters()
        }
    } else {
        router.push('/login')
    }
})


// Opens input for adding new chapter
function toggleEdit() {
  edit_store.setEdit(addId)
}

// Sends changes to backend
function saveChanges() {

}
// END saveChanges
</script>


<template>
    <div id="panel" class="shadow-2xl flex flex-col gap-4 overflow-y-auto">  
        <div class="text-m breadcrumbs">
            <ul>
                <li><RouterLink to="/courses">Courses</RouterLink></li> 
                <li><a>Selected course</a></li> 
            </ul>
        </div> 

        <EditChapterModal />
        <div class="divider">Chapters</div>

        <!-- selectedChapters returns the chapters rather than storing state copy -->
        <div class="flex flex-col gap-3 mt-3">
            <ChapterCard v-for="chapter in chapter_store.selectedChapters()" :id="chapter.id" :title="chapter.title" />
        </div>

        <AddChapter v-show="edit_store.isEdit(addId)" />    

        <div class="divider">Add new</div>
        <div class="card">
            <button class="btn btn-primary" @click="toggleEdit">Add Chapter</button>  
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