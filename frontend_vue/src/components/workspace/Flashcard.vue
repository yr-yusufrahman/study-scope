<script setup>


defineProps({
  id: Number,
  question: String,
  answer: String,
  order: Number
})

</script>


<template>
    <div class="rounded-xl shadow-md bg-base-100 p-3 new-line">
        <div class="flex w-full flex-row">
            <div class="w-1/3 break-words">
                <p>{{ question }}</p>
            </div> 
            <div class="divider divider-horizontal"></div> 
            <div class="w-2/3 break-words">
                <p>{{ answer }}</p>
            </div>
            <div>
                <button class="btn btn-ghost break-normal">Edit</button>
            </div>
        </div>
    </div>
</template>


<style scoped>
</style>