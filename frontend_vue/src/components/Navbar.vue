<script setup>
import { RouterLink } from 'vue-router'

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('refresh');
}
</script>


<template>
  <div id="navbar" class="navbar bg-base-100">
    <div id="nav-logo" class="flex-1">
      <RouterLink to="/" class="btn btn-ghost text-xl">Study App</RouterLink>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        <li><RouterLink to="/login">Login</RouterLink></li>
        <li>
          <details>
            <summary>Parent</summary>
            <ul class="p-2 bg-base-100 rounded-t-none">
              <li><a>Link 1</a></li>
              <li><RouterLink to="/" @click="logout">Logout</RouterLink></li>
            </ul>
          </details>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
#navbar {
  background-image: linear-gradient(45deg, #7BCDC8, #35ACDA);
}

div {
  color: white;
}

details ul li {
  color: initial;
}

</style>