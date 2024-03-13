<script setup>
import Landing from '../components/Landing.vue'
import Bottom from '@/components/Bottom.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// Check for logged in
const token = localStorage.getItem('token')
if (token) {
  router.push('/courses')
}
</script>

<template>
  <main>
    <Landing />
  </main>
  <footer>
    <Bottom />
  </footer>
</template>
