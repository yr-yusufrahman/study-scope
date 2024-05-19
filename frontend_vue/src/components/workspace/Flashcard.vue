<script setup>


defineProps({
  id: Number,
  question: String,
  answer: String,
  order: Number
})

</script>


<template>
    <div class="rounded-xl shadow-md bg-base-100 p-3">
        <div class="flex w-full flex-row">
            <div class="w-1/3 break-words">
                <p>{{ question }}</p>
            </div> 
            <div class="divider divider-horizontal"></div> 
            <div class="w-2/3 break-words">
                <p>{{ answer }}</p>
            </div>
        </div>
        <p>Order: {{ order }}</p>
        <p>Id: {{ id }}</p>
    </div>
</template>


<style scoped>
</style>