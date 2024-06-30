<script setup>
import EditChapterModal from './EditChapterModal.vue'
import ChapterCard from './ChapterCard.vue'
import AddChapter from './AddChapter.vue'
import ConfirmModal from '../helpers/ConfirmModal.vue'

import { useRouter } from 'vue-router'
import { RouterLink, onBeforeRouteLeave } from 'vue-router'
import { ref, onUnmounted, onMounted, onBeforeMount } from 'vue'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import logout from '../helpers/logout.js'

const router = useRouter()

const chapter_store = useChapterStore()
const edit_store = useToggleEditStore()

const addId = -1


// Redirect to courses page if no course selected
onBeforeMount(() => {
		const state_course = chapter_store.getCourse

		const makeRequest = () => {
				const request = chapter_store.getChaptersRequest()
				request.then((success) => {
						if (!success) {
								logout()
								router.push('/login')
						}
				})
		}

		// If there is no chapter in state, check storage
		if (state_course) {
				makeRequest()
				return
		} else {
				// Local storage is just for persisting on refresh
				const course = Number(localStorage.getItem('selectedCourse'))
				if (course) {
						chapter_store.selectCourse(course)
						makeRequest()
						return
				} else {
						router.push('/courses')
				}
		}
})


// Autosave changes when leaving the page
onBeforeRouteLeave((to, from) => {
  if (chapter_store.isModified) {
    chapter_store.saveChaptersRequest()
  }
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
	const request = chapter_store.saveChaptersRequest()
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
								:drag="false"
						/>
				</div>

				<AddChapter v-show="edit_store.isEdit(addId)" />    

				<div class="divider">Add new</div>
				<div>
						<button class="btn btn-primary" @click="toggleEdit">Add Chapter</button>  
						<button class="btn btn-accent" @click="saveChanges">Save Changes</button>    
				</div>
				
				<ConfirmModal :remove="true" />
							
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