<script setup>
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '@/stores/ChapterStore';
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

const course_store = useCourseStore()
const chapter_store = useChapterStore()
const edit_store = useToggleEditStore()

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
</script>


<template>
    <!-- Put this part before </body> tag -->
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
</template>


