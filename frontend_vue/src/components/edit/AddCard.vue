<script setup>
import { ref, nextTick, onMounted, watch, onUpdated } from 'vue'
import { useCardStore } from '../../stores/CardStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import autoResize from '../helpers/textResize.js'

const props = defineProps({
  addIndex: Number,
})

// State
const card_store = useCardStore()
const edit_store = useToggleEditStore()
const new_question = ref('')
const new_answer = ref('')
const form = ref(null)


// Focuses question input for adding card by watching edit store, the value is the result of isEdit
watch(() => edit_store.isEdit(props.addIndex), (value) => {
    if (value) {
        nextTick(() => {
            new_question.value.focus()
        })
    }
})


// Focuses question input after adding card
onUpdated(() => new_question.value.focus())


// Adds new chapter
function handleAdd(form_data) {
    const question_input = form_data[0]
    const answer_input = form_data[1]

    const new_question = question_input.value
    const new_answer = answer_input.value
    const new_index = props.addIndex + 1
    if (new_question.trim() !== '') {
        card_store.addCard(new_question, new_answer, new_index)

        // Clear input fields
        question_input.value = ''
        answer_input.value = ''
        question_input.style.height = '3rem'
        edit_store.setEdit(new_index)
    }
}


function close() {
    edit_store.setEdit(null)
}
</script>


<template>
    <div class="rounded-xl shadow-md p-3 bg-base-100 border-2 border-solid border-sky-400">

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
        <form @submit.prevent="handleAdd(form)" ref="form" >
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
                        @input="autoResize($event.target)"
                    ></textarea>
                </div>
            </div>
            
            <!-- Submit button -->
            <div class="form-control mt-6">
                <button class="btn bg-teal-100" >Add</button>
            </div>
        </form>
    </div>
</template>
