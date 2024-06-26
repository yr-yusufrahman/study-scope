<script setup>
import EditChapterModal from './EditChapterModal.vue'
import ChapterCard from './ChapterCard.vue'
import AddChapter from './AddChapter.vue'
import ConfirmModal from '../helpers/ConfirmModal.vue'

import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { ref, onUnmounted, onMounted, onBeforeMount } from 'vue'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import logout from '../helpers/logout.js'

const router = useRouter()

const chapter_store = useChapterStore()
const edit_store = useToggleEditStore()

// State
const course_name = ref('')
const addId = -1


onBeforeMount(() => {
    const course = Number(localStorage.getItem('selectedCourse'))
    if (!course) {
        router.push('/courses')
        return
    } else if (course !== chapter_store.getCourse) {
        chapter_store.selectCourse(course)
    }

    const makeRequest = () => {
        const request = chapter_store.getChaptersRequest()
        request.then((success) => {
            if (!success) {
                logout()
                router.push('/login')
            }
        })
    }
    makeRequest()
})



// Before leaving
onUnmounted(() => {
    edit_store.clear()
})


// Opens input for adding new chapter
function toggleEdit() {
  edit_store.setEdit(addId)
}

// Sends changes to backend
function saveChanges() {
    let success = chapter_store.saveChaptersRequest()
    if (!success) {
        router.push('/login')
    }
}
// END saveChanges
</script>


<template>
    <div id="panel" class="shadow-2xl flex flex-col gap-1 fixed">
        <div class=" h-16"></div>

        <div class="text-m breadcrumbs overflow-x-clip">
            <ul class="whitespace-normal">
                <li><RouterLink to="/courses">Courses</RouterLink></li> 
                <li><p>{{ chapter_store.getCourseName }}</p></li> 
            </ul>
        </div> 

        <EditChapterModal />
        <div class="divider">Chapters</div>

        <!-- selectedChapters returns the chapters rather than storing state copy -->
        <div class="flex flex-col gap-2 pr-1 overflow-y-auto min-h-28 pb-28" >
            <ChapterCard 
                v-for="(chapter, index) in chapter_store.getChapters" 
                :id="chapter.id" 
                :title="chapter.title"
                :due="chapter.next_due"
                :key="index"
            />
        </div>

        <AddChapter v-show="edit_store.isEdit(addId)" />    

        <div class="divider">Add new</div>
        <div>
            <button class="btn btn-primary" @click="toggleEdit">Add Chapter</button>  
            <button class="btn btn-accent" @click="saveChanges">Save Changes</button>    
        </div>
        
        <ConfirmModal />
              
    </div>
</template>


<style scoped>
#panel {
    height: 100%;
    padding: 0.5rem;
    background-color: white;
    width: 23%;
    max-width: 350px;
}

</style>