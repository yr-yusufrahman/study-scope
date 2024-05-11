<script setup>
import { ref, nextTick } from 'vue'
import { useChapterStore } from '@/stores/ChapterStore'
import { useCardStore } from '@/stores/CardStore'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

defineProps({
  id: Number,
  title: String,
})

const chapter_store = useChapterStore()
const card_store = useCardStore()
const edit_store = useToggleEditStore()
const input = ref('')


// Selects chapter to view flashcards
function selectChapter(id) {
  card_store.setChapter(id)
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
function handleEdit(e, id, original_title) {
  /**/
  const new_title = e.target[0].value
  if (new_title !== original_title) {
    chapter_store.editChapter(id, new_title)
  } else {
    console.log('Chapter already exists with this name')
  }
  edit_store.setEdit(id)
  
}

// Deletes chapter
function handleDelete(id) {
  chapter_store.removeChapter(id)
}

</script>


<template>
  <div class=" flex flex-row bg-base-200 rounded-lg">
    <div class=" w-full">
      <button v-show="!edit_store.isEdit(id)" @click="selectChapter(id)" class="btn btn-ghost">{{ title }}</button>

      <form v-show="edit_store.isEdit(id)" @submit.prevent="(event) => handleEdit(event, id, title)">
        <input ref="input" :value=title type="text" placeholder="Title" class="input input-bordered" />  
      </form>
    </div>  

    <div class="dropdown dropdown-hover">
      <div tabindex="0" role="button" class="btn" >...</div>
      <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
        <li><button @click="toggleEdit(id)">Edit</button></li>
        <li><button @click="handleDelete(id)">Delete</button></li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.dropdown {
  position: initial;
}
</style>