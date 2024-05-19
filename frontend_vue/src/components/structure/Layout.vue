<script setup>
import { RouterView } from 'vue-router'
import Navbar from './Navbar.vue'
</script>


<template>
  <header>
    <nav>
      <Navbar />
    </nav>
  </header>

  <div class="">
    <RouterView />  
  </div>
</template>