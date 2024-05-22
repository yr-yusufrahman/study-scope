<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useChapterStore } from '../../stores/ChapterStore.js'
import { useCardStore } from '../../stores/CardStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import autoResize from '../helpers/textResize.js'

const props = defineProps({
  addIndex: Number,
})

// State
const store = useCourseStore()
const chapter_store = useChapterStore()
const card_store = useCardStore()
const edit_store = useToggleEditStore()
const new_question = ref('')
const new_answer = ref('')


// Focuses input for adding new chapter by watching for edit state, the value is the result of isEdit
watch(() => edit_store.isEdit(props.addIndex), (value) => {
    if (value) {
        nextTick(() => {
            new_question.value.focus()
        })
    }
})


// Adds new chapter
function handleAdd(e) {
    /*
    const new_title = e.target[0]
    const new_chapter = new_title.value
    let success = chapter_store.addChapter(new_chapter)
    if (success) {
        new_title.value = ''
    } else {
        console.log('Failed to add chapter')
    }*/
}


function close() {
    edit_store.setEdit(null)
}
</script>


<template>
    <div class="rounded-xl shadow-md bg-base-100 p-3">

        <!-- Move and delete add card input -->
        <div class="flex flex-row w-full pb-3">
            <div class="flex w-full pl-3 items-center">
                <p>Question</p>
                <div class="w-1/3"></div>
                <p>Answer</p>
                <div class=" w-5/12"></div>
                <button class="btn btn-ghost">Move</button>          
            </div>
            
            <button class="btn btn-error" @click="close">Delete</button>
        </div>

        <!-- Add card input -->
        <form @submit.prevent="handleAdd" >
            <div class="form-control">
                <div class="flex w-full flex-row">
                    <textarea
                        rows="1"
                        ref="new_question" 
                        type="text" 
                        placeholder="Question" 
                        class="w-1/3 card-edit textarea textarea-bordered break-words overflow-y-hidden" 
                        required
                        @input="autoResize($event.target)"
                    ></textarea> 

                    <div class="divider divider-horizontal"></div>
                    <textarea
                        rows="1"
                        ref="new_answer"
                        type="text"
                        placeholder="Answer"
                        class="w-2/3 card-edit textarea textarea-bordered break-words overflow-y-hidden"
                        required
                        @input="autoResize($event.target)"
                    ></textarea>
                </div>
            </div>
            
            <!-- Submit button -->
            <div class="form-control mt-6">
                <button class="btn bg-teal-100">Add</button>
            </div>
        </form>
    </div>
</template>
