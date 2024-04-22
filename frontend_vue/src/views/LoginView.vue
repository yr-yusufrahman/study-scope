<script setup>
import LoginForm from '@/components/login/LoginForm.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// Check for logged in
const token = localStorage.getItem('token')
if (token) {
  router.push('/courses')
}
</script>


<template>
  <div class="bg">
    <LoginForm />  
  </div>
</template>


