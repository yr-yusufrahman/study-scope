<script setup>
import { onMounted, ref } from 'vue'
import AddCard from './AddCard.vue'
import { useCardStore } from '@/stores/CardStore';
import { useToggleEditStore } from '@/stores/ToggleEditStore';
import autoResize from '../helpers/textResize.js'

defineProps({
    id: Number,
    question: String,
    answer: String,
    order: Number,
    addIndex: Number
})

const card_store = useCardStore()
const edit_store = useToggleEditStore()
const add_below = ref(false)
const new_question = ref('')
const new_answer = ref('')
const dragging = ref(false)
const scrollInterval = ref(null)
const item = ref(null)

// Resize textareas
onMounted(() => {
    autoResize(new_question.value)
    autoResize(new_answer.value)
})


// Opens input for adding new card
function toggleEdit(addIndex) {
  edit_store.setEdit(addIndex)
}


// Deletes card
function handleDelete(id) {
    card_store.removeCard(id)
}


// This function should run after the user clicks outside the textarea
function handleEdit(id, original_question, original_answer) {
    const edit_question = new_question.value.value
    const edit_answer = new_answer.value.value

    if (edit_question !== original_question || edit_answer !== original_answer) {
        card_store.editCard(id, edit_question, edit_answer)
    }
}

function dragState(state) {
    dragging.value = state
}

// Allows dragging of cards
function startDrag(e, id) {
    dragging.value = true
    e.dataTransfer.dropEffect = 'move'
    e.dataTransfer.effectAllowed = 'move'
    card_store.setDragging(id)
    //startAutoScroll()
}

function stopDrag() {
    dragging.value = false
    card_store.setDragging(null)
    //stopAutoScroll()
}

// --- Auto scroll when dragging ---

// When the dragged card is near the bottom of the window (viewport), the window should scroll down
// When the dragged card is near the top of the window, below navbar (viewport), the window should scroll up

function startAutoScroll() {
    /*
    scrollInterval.value = setInterval(() => {
        const scrollBuffer = 50
        const scrollSpeed = 10
        const card = document.querySelector('.dragging')
        const rect = card.getBoundingClientRect()

        if (rect) {}
    }, 16)
    */
    scrollInterval.value = setInterval(() => {
        const card = item.value
        console.log(card)
        /*
        //const rect = card.getBoundingClientRect()
        const top = rect.top
        const bottom = rect.bottom
        const height = rect.height
        const scrollSpeed = 10

        if (top < 0) {
            window.scrollBy(0, -scrollSpeed)
        } else if (bottom > window.innerHeight) {
            window.scrollBy(0, scrollSpeed)
        }*/

    }, 16)
    
}

function stopAutoScroll() {
    clearInterval(scrollInterval)
    scrollInterval.value = null
}

</script>


<template>
    <div 
        name="card"
        :class="{'dragging': dragging}"
        :draggable="dragging" 
        @dragstart="startDrag($event, id)" 
        @dragend="stopDrag()"
        ref="item"
    >
        <!-- Card contents -->
        <div class="rounded-xl shadow-md bg-base-100 p-4 w-full" >
            <!-- Move and delete button header -->
            <div class="flex flex-row w-full pb-3 items-center">

                <!-- Draggable -->
                <div class="w-full drag-cursor" @mousedown="dragState(true)" @mouseup="dragState(false)">
                    <button class="btn btn-ghost">Move</button>    
                </div>
                
                <button class="btn btn-error" @click="handleDelete(id)">Delete</button>
            </div>

            <!-- Question and answer input -->
            <div class="flex w-full flex-row">
                <label class="form-control w-1/3">
                    <textarea
                        id="question"
                        :value="question"
                        placeholder="Question" 
                        ref="new_question" 
                        type="text" 
                        required
                        @input="autoResize($event.target)"
                        @focusout="handleEdit(id, question, answer)"      
                        class="w-full card-edit textarea textarea-bordered break-words overflow-y-hidden" 
                    ></textarea> 

                    <div class="label">
                        <span class="label-text-alt">Question</span>
                    </div>
                </label>

                <div class="divider divider-horizontal"></div> 

                <label class="form-control w-2/3">
                    <textarea
                        id="answer"
                        :value="answer"
                        placeholder="Answer" 
                        ref="new_answer" 
                        type="text" 
                        required
                        @input="autoResize($event.target)"
                        @focusout="handleEdit(id, question, answer)"          
                        class="w-full card-edit textarea textarea-bordered break-words overflow-y-hidden" 
                    ></textarea>

                    <div class="label">
                        <span class="label-text-alt">Answer</span>
                    </div>
                </label>
            </div>
        </div>
        
        <!-- Gap between cards and add card button -->
        <div class="h-7" >
            <div
                class="w-full h-full flex justify-center"
                v-show="!edit_store.isEdit(addIndex) && (card_store.getCards.length-1 !== addIndex)" 
                @mouseover="add_below = true" 
                @mouseleave="add_below = false"            
            >
                <Transition>    
                    <button
                        v-show="add_below"
                        class="btn btn-info absolute"
                        @click="toggleEdit(addIndex)"
                        @mouseover="add_below = true" 
                        @mouseleave="add_below = false"
                    >Add Card</button>
                </Transition>
            </div>
        </div>

        <!-- Add input below this specific card -->
        <Transition>
            <div class=" pb-7" v-show="edit_store.isEdit(addIndex) && (card_store.getCards.length-1 !== addIndex)">
                <AddCard class="w-full" :add-index="addIndex" />    
            </div>
        </Transition>
    </div>
</template>


<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>