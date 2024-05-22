<script setup>
import { onMounted, ref } from 'vue'
import AddCard from './AddCard.vue'
import { useToggleEditStore } from '@/stores/ToggleEditStore';
import autoResize from '../helpers/textResize.js'

defineProps({
    id: Number,
    question: String,
    answer: String,
    order: Number,
    lastAdd: Boolean,
    addIndex: Number
})

const edit_store = useToggleEditStore()
const add_below = ref(false)
const new_question = ref('')
const new_answer = ref('')

// Resize textareas
onMounted(() => {
    autoResize(new_question.value)
    autoResize(new_answer.value)
})


// Opens input for adding new card
function toggleEdit(addIndex) {
  edit_store.setEdit(addIndex)
}


function handleDelete(id) {
    console.log('Delete card:', id)
}
</script>


<template>
    <div>
        <!-- Card contents -->
        <div class="rounded-xl shadow-md bg-base-100 p-4 w-full">
            <!-- Move and delete button header -->
            <div class="flex flex-row w-full pb-3">
                <div class="flex w-full pl-3 items-center">
                    <p>Question</p>
                    <div class="w-1/3"></div>
                    <p>Answer</p>
                    <div class=" w-5/12"></div>
                    <button class="btn btn-ghost">Move</button>          
                </div>
                
                <button class="btn btn-error" @click="handleDelete(id)">Delete</button>
            </div>

            <!-- Question and answer input -->
            <div class="flex w-full flex-row">           
                <textarea
                    :value="question"
                    placeholder="Question" 
                    ref="new_question" 
                    type="text" 
                    required
                    @input="autoResize($event.target)"                
                    class="w-1/3 card-edit textarea textarea-bordered break-words overflow-y-hidden" 
                ></textarea> 

                <div class="divider divider-horizontal"></div> 

                <textarea
                    :value="answer"
                    placeholder="Answer" 
                    ref="new_answer" 
                    type="text" 
                    required
                    @input="autoResize($event.target)"                
                    class="w-2/3 card-edit textarea textarea-bordered break-words overflow-y-hidden" 
                ></textarea> 
            </div>
        </div>
        
        <!-- Gap between cards and add card button -->
        <div class="flex justify-center h-7" 
            v-show="lastAdd && !edit_store.isEdit(addIndex)" 
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

        <!-- Add input below this specific card -->
        <div class="pt-7 pb-7" v-show="lastAdd && edit_store.isEdit(addIndex)">
            <AddCard class="w-full" :add-index="addIndex" />    
        </div>
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