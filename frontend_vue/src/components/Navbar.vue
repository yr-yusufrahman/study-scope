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
      <button class="btn btn-ghost rounded-btn">
        <RouterLink to="/login">Login</RouterLink>  
      </button>
      
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost rounded-btn">Dropdown</div>
        <ul tabindex="0" class="menu dropdown-content z-[1] p-2 shadow bg-base-100 rounded-box w-52 mt-4">
          <li><a>Item 1</a></li> 
          <li><RouterLink to="/" @click="logout">Logout</RouterLink></li>
        </ul>
      </div>
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

.dropdown ul li {
  color: initial;
}

</style>