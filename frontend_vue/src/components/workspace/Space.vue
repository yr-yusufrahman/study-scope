<script setup>
import FlashcardArea from './FlashcardArea.vue';

import ChapterDirectory from './ChapterDirectory.vue';
import { RouterLink } from 'vue-router';
</script>


<template>
  <div class="layout grid grid-cols-10">

    <div class="col-span-3">
      <ChapterDirectory />
    </div>
    <div class="col-span-7">
      <FlashcardArea />
    </div>

  </div>
</template>


<style scoped>
.layout {
  height: 80vh;
}
</style>