<script setup>
import { useCourseStore } from '../../stores/CourseStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

const course_store = useCourseStore()
const edit_store = useToggleEditStore()

function handleDelete() {
    const type = edit_store.getDeleteModal
    if (type === 0) {
        const id = course_store.getDeleting
        course_store.removeCourse(id)
    }
}
</script>


<template>
    <!-- Put this part before </body> tag -->
    <input type="checkbox" id="my_modal_7" class="modal-toggle" />
    <div class="modal" role="dialog">
        <div class="modal-box">
            <h3 class="text-lg font-bold">Wait!</h3>
            <p class="py-4">Are you sure you want to delete this item? All associated data will be lost.</p>
            <div class="modal-action flex flex-row justify-around">
                <label for="my_modal_7" class="btn btn-error" @click="handleDelete">Delete</label>
                <label for="my_modal_7" class="btn">Close!</label>
            </div>            
        </div>
    </div>
</template>


