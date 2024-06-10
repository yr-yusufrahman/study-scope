<script setup>
import { ref, nextTick } from 'vue'
import { useChapterStore } from '@/stores/ChapterStore'
import { useCardStore } from '@/stores/CardStore'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'
import autoResize from '../helpers/textResize'

const props = defineProps({
  id: Number,
  title: String,
})

const chapter_store = useChapterStore()
const card_store = useCardStore()
const edit_store = useToggleEditStore()
const input = ref('')
const form = ref(null)


// Selects chapter to view flashcards
function selectChapter() {
  const id = props.id
  const title = props.title
  card_store.setChapter(id, title)
  //localStorage.setItem('selectedChapter', id)
}


// Opens input for editing chapter title
function toggleEdit(id) {
  edit_store.setEdit(id)

  // Focus on input after DOM renders
  nextTick(() => {
    input.value.focus()
  })
}


// Handles editing chapter title
function handleEdit(form_data, id, original_title) {
  const new_title = form_data[0]
  const new_chapter = new_title.value

  if (new_chapter !== original_title && new_chapter.trim() !== '') {
    chapter_store.editChapter(id, new_chapter)
  } else {
    console.log('Chapter already exists with this name or empty input.')
    new_title.value = original_title
  }

  // Close edit input
  edit_store.setEdit(id)
}

// Deletes chapter
function handleDelete(id) {
  chapter_store.removeChapter(id)
}

</script>


<template>
  <div class=" flex flex-row bg-base-200 rounded-lg p-1">
    <div class=" w-full">
      <button v-show="!edit_store.isEdit(id)" @click="selectChapter()" class="btn btn-ghost h-auto chapter-name">{{ title }}</button>


      <form ref="form" v-show="edit_store.isEdit(id)" @submit.prevent="handleEdit(form, id, title)">
        <!-- 
        <input ref="input" :value=title type="text" placeholder="Title" class="input input-bordered" />  
        -->
        <textarea 
          rows="1"
          ref="input" 
          :value=title
          type="text" 
          placeholder="Title" 
          class="textarea textarea-bordered card-edit overflow-y-hidden" 
          required
          @input="autoResize($event.target)"
          @keydown.enter.prevent="handleEdit(form, id, title)"
        ></textarea>
      </form>
    </div>  

    <div class="relative dropdown dropdown-hover">
      <div tabindex="0" role="button" class="btn" >...</div>
      <ul tabindex="0" class="absolute glass-light dropdown-content z-[1] menu p-2 shadow rounded-box right-0">
        <li><button @click="toggleEdit(id)">Edit</button></li>
        <li><button @click="handleDelete(id)">Delete</button></li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.chapter-name {
  font-weight: bold;
  word-break: break-word;
}
</style>