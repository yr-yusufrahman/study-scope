<script setup>
import { onMounted, ref } from 'vue';
import autoResize from '../helpers/textResize.js'

defineProps({
  id: Number,
  question: String,
  answer: String,
  order: Number
})

const new_question = ref('')
const new_answer = ref('')

// Resize textareas
onMounted(() => {
    autoResize(new_question.value)
    autoResize(new_answer.value)
})

function handleDelete(id) {
    console.log('Delete card:', id)
}
</script>


<template>
    <div class="rounded-xl shadow-md bg-base-100 p-3 w-full">
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
        <div class="flex w-full h-8 justify-center">
            <div>Add below</div>
        </div>

    </div>
</template>