<script setup>
import Navbar from '@/components/structure/Navbar.vue'
import EditArea from '../components/edit/EditArea.vue'
</script>

<template>
    <header>
        <nav>
            <Navbar />
        </nav>
    </header>

    <main class="bg pt-16">
        <EditArea />
    </main>
</template>