<script setup>
import GoogleLoginButton from './GoogleLoginButton.vue';
import { useRouter } from 'vue-router'
import axios from 'axios'

// Checks for code in URL and sends it to the backend
function googleAuth() {
  const url_params = new URLSearchParams(window.location.search)
  const code = url_params.get('code')

  if (code) {
    const google_auth = "http://127.0.0.1:8000/auth/google"
    const request_data = {
      code: code
    }
    
    axios.post(google_auth, request_data)
      .then(response => {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('refresh', response.data.refresh_token)
        localStorage.setItem('email', response.data.email)
        localStorage.setItem('name', response.data.name)
        router.push('/courses')
      })
    /*
    fetch(google_auth, requestOptions)
      .then(response => response.json())
      .then(data => {
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('refresh', data.refresh_token)
        localStorage.setItem('email', data.email)
        localStorage.setItem('name', data.name)
        router.push('/courses')
      })
    */
  }
}
// END googleAuth

const router = useRouter()
const isDev = import.meta.env.DEV
const google_login = 'http://127.0.0.1:8000/login/google'
const dev_bypass_url = 'http://127.0.0.1:8000/auth/dev-login'

function devBypassLogin() {
  axios.post(dev_bypass_url)
    .then(response => {
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('refresh', response.data.refresh_token)
      localStorage.setItem('email', response.data.email)
      localStorage.setItem('name', response.data.name)
      router.push('/courses')
    })
    .catch(error => {
      console.log('Dev login failed', error)
    })
}

googleAuth()
</script>

<template>
  <div class="hero min-h-screen">
    <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <a :href="google_login" >
          <GoogleLoginButton />
        </a>
        <button
          v-if="isDev"
          type="button"
          class="btn btn-outline btn-secondary mt-4 w-full"
          @click="devBypassLogin"
        >
          Continue as saved account (dev only)
        </button>
      </div>
    </div>
  </div>
  <br>
  
</template>