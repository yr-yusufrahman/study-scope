<script setup>
import Navbar from '@/components/structure/Navbar.vue'
import CourseList from '@/components/courses/CourseList.vue'
</script>


<template>
  <header>
    <nav>
      <Navbar />
    </nav>
  </header>

  <main class="bg min-h-screen pt-20 px-8 pb-16">
    <CourseList />
  </main>
</template>
