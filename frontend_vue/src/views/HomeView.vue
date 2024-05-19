<script setup>
import Landing from '../components/structure/Landing.vue'
import Bottom from '../components/structure/Bottom.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// Check for logged in
const token = localStorage.getItem('token')
if (token) {
  router.push('/courses')
}
</script>

<template>
  <div class=" pt-16">
    <main>
      <Landing />
    </main>
    <footer>
      <Bottom />
    </footer>
  </div>
</template>
