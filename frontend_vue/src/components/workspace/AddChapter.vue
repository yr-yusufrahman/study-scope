<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

// State
const store = useCourseStore()
const chapter_store = useChapterStore()
const edit_store = useToggleEditStore()
const addId = -1
const new_title = ref('')


// Focuses input for adding new chapter by watching for edit state
watch(() => edit_store.isEdit(addId), (value) => {
    if (value) {
        nextTick(() => {
            new_title.value.focus()
        })
    }
})


// Adds new chapter
function handleAdd(e) {
    const new_title = e.target[0]
    const new_chapter = new_title.value
    let success = chapter_store.addChapter(new_chapter)
    if (success) {
        new_title.value = ''
    } else {
        console.log('Failed to add chapter')
    }
}
</script>


<template>
    <form @submit.prevent="handleAdd" >
        <div class="form-control">
            <label class="label">
                <span class="label-text">Chapter name</span>
            </label>
            <input ref="new_title" type="text" placeholder="Title" class="input input-bordered" required />
        </div>
        <div class="form-control mt-6">
            <button class="btn bg-teal-100">Add</button>
        </div>
    </form>
</template>
