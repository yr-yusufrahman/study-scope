<script setup>
import FlashcardArea from './FlashcardArea.vue';
import ChapterDirectory from './ChapterDirectory.vue';
</script>


<template>
  <div class="layout flex flex-row">
    
    <div class="directory">
      <ChapterDirectory />  
    </div>

    <div id="card-area">
      <FlashcardArea />
    </div>
  </div>
</template>


<style scoped>
.layout {
  height: 80vh;
}

.directory {
  width: 30vw;
  max-width: 350px;
}

#card-area {
  width: 100%;
  padding-top: 4rem;
  display: flex;
  justify-content: center;
}
</style>