<script setup>
import { ref, nextTick } from 'vue'
import { useCourseStore } from '../../stores/CourseStore.js'
import { useToggleEditStore } from '../../stores/ToggleEditStore.js'

defineProps({
  id: Number,
  title: String,
})

const store = useCourseStore()
const edit_store = useToggleEditStore()
const input = ref('')


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
    store.editChapter(id, new_title)
  } else {
    console.log('Chapter already exists with this name')
  }
  edit_store.setEdit(id)
  
}

// Deletes chapter
function handleDelete(e) {
  /*
  const id = Number(e.target.value)
  store.removeCourse(id)
  */
}

</script>


<template>
  <div class="grid grid-cols-8 bg-base-200 rounded-lg">
    <div class="col-span-7">
      <button v-show="!edit_store.isEdit(id)" class="btn btn-ghost">{{ title }}</button>

      <form v-show="edit_store.isEdit(id)" @submit.prevent="(event) => handleEdit(event, id, title)">
        <input ref="input" :value=title type="text" placeholder="Title" class="input input-bordered" />  
      </form>

    </div>
    <div class="col-span-1 flex flex-row gap-1">
      <button @click="toggleEdit(id)">Edit</button>
    </div>
  </div>
</template>

<style scoped>
</style>