<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import autoResize from '../helpers/textResize.js'

// State
const store = useCourseStore()
const chapter_store = useChapterStore()
const edit_store = useToggleEditStore()
const addId = -1
const new_title = ref('')
const form = ref(null)


// Focuses input for adding new chapter by watching for edit state
watch(() => edit_store.isEdit(addId), (value) => {
    if (value) {
        nextTick(() => {
            new_title.value.focus()
        })
    }
})


// Adds new chapter
function handleAdd(form_data) {
    const new_title = form_data[0]
    const new_chapter = new_title.value
    if (new_chapter.trim() !== '') {

        let success = chapter_store.addChapter(new_chapter)
        if (success) {
            new_title.value = ''
            new_title.style.height = '3rem'
        } else {
            console.log('Failed to add chapter')
        }
    }
}


</script>


<template>
    <form @submit.prevent="handleAdd(form)" ref="form" class=" mt-1">
        <div class="form-control">
            <!--
            <input ref="new_title" type="text" placeholder="Title" class="input input-bordered" required />-->
            <textarea 
                rows="1"
                ref="new_title" 
                type="text" 
                placeholder="Title" 
                class="textarea textarea-bordered card-edit overflow-y-hidden" 
                required
                @input="autoResize($event.target)"
                @keydown.enter.prevent="handleAdd(form)"
            ></textarea>
        </div>
        <div class="form-control mt-6">
            <button class="btn bg-teal-100">Add</button>
        </div>
    </form>
</template>
