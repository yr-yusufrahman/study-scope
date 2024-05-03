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
  edit_store.setEditCourse(id)

  // Focus on input after DOM renders
  nextTick(() => {
    input.value.focus()
  })
}


// Handles editing chapter title
function handleEdit(e, id, original_title) {
  /*
  id = Number(id)
  const new_title = e.target[0].value
  if (new_title !== original_title && !store.courseExists(new_title)) {
    store.editCourse(id, new_title)
  } else {
    console.log('Course already exists with this name')
  }
  edit_store.setEditCourse(id)
  */
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
      <button class="btn btn-ghost">{{ title }}</button>
    </div>
    <div class="col-span-1 flex flex-row gap-1">
      <button>Name</button>
    </div>
  </div>
</template>

<style scoped>
</style>