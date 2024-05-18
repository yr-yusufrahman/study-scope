<script setup>
import { RouterLink } from 'vue-router'

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('refresh');
}
</script>


<template>
  <div id="navbar" class="navbar">
    <div id="nav-logo" class="flex-1">
      <RouterLink to="/" class="btn btn-ghost text-xl">Study App</RouterLink>
    </div>
    <div class="flex-none">
      <button class="btn btn-ghost rounded-btn">
        <RouterLink to="/login">Login</RouterLink>  
      </button>
      
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost rounded-btn">Dropdown</div>
        <ul tabindex="0" class="glass-light dropdown-content z-[1] menu p-2 shadow-xl rounded-box w-52">
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
  position: fixed;
  z-index: 1;
}

div {
  color: white;
}

.dropdown ul li {
  color: initial;
}

</style>