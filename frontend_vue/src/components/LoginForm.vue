<script setup>
import GoogleLoginButton from './GoogleLoginButton.vue';
import { useRouter } from 'vue-router'

// Checks for code in URL and sends it to the backend
function googleAuth() {
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')

  if (code) {
    const google_auth = "http://127.0.0.1:8000/auth/google"
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code })
    }

    fetch(google_auth, requestOptions)
      .then(response => response.json())
      .then(data => {
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('email', data.email)
        localStorage.setItem('name', data.name)
        router.push('/courses')
      })

  }
}
// END googleAuth

const router = useRouter()
const google_login = 'http://127.0.0.1:8000/login/google'

googleAuth()
</script>

<template>
  <div class="hero min-h-screen bg-base-200">
    <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <a :href="google_login" >
          <GoogleLoginButton />
        </a>
      </div>
    </div>
  </div>
  <br>
  
</template>./GoogleLoginButton.vue