<script setup>
import { useRouter } from 'vue-router'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '@/stores/ChapterStore';
import { useCardStore } from '@/stores/CardStore';
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'


const props = defineProps({
  remove: Boolean
})

const router = useRouter()

const course_store = useCourseStore()
const chapter_store = useChapterStore()
const card_store = useCardStore()
const edit_store = useToggleEditStore()


// Delete item
function handleDelete() {
	const type = edit_store.getDeleteModal
	if (type === 0) {
		const id = edit_store.getDeleting
		course_store.removeCourse(id)
	} else if (type === 1) {
		const id = edit_store.getDeleting
		chapter_store.removeChapter(id)
	}
}

// Save changes before leaving
function handleSave() {
	const type = edit_store.getSaveModal
	if (type === 0) {
		course_store.saveCoursesRequest()
	} else if (type === 1) {
		chapter_store.saveChaptersRequest()
	} else if (type === 2) {
		card_store.saveCardsRequest()
	}

}

function close() {
	const redirect = edit_store.getRedirect
	router.push(redirect)
}
</script>


<template>
	<section v-show="remove">
		<input type="checkbox" id="delete_modal" class="modal-toggle" />
		<div class="modal" role="dialog">
			<div class="modal-box">
				<h3 class="text-lg font-bold">Wait!</h3>
				<p class="py-4">Are you sure you want to delete this item? All associated data will be lost.</p>
				<div class="modal-action flex flex-row justify-around">
					<label for="delete_modal" class="btn btn-error" @click="handleDelete">Delete</label>
					<label for="delete_modal" class="btn">Close!</label>
				</div>            
			</div>
		</div>
	</section>

	<section v-show="!remove">
		<input type="checkbox" id="save_modal" class="modal-toggle" />
		<div class="modal" role="dialog">
			<div class="modal-box">
				<h3 class="text-lg font-bold">Wait!</h3>
				<p class="py-4">Any unsaved changes will be lost!</p>
				<div class="modal-action flex flex-row justify-around">
					<label for="save_modal" class="btn btn-info" @click="handleSave">Save</label>
					<label for="save_modal" class="btn" @click="close">Exit</label>
				</div>            
			</div>
		</div>
	</section>
</template>


