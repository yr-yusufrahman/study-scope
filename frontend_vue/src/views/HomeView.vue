<script setup>
import Landing from '../components/structure/Landing.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// Check for logged in
const token = localStorage.getItem('token')
if (token) {
  router.push('/dashboard')
}
</script>

<template>
  <div class="bg min-h-screen">
    <main>
      <Landing />
    </main>
  </div>
</template>
