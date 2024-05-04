<script setup>
</script>

<!-- Used to delete and move chapters in the directory -->
<template>
    <!-- The button to open modal -->
    <label for="my_modal_7" class="btn btn-info">Options</label>

    <!-- Put this part before </body> tag -->
    <input type="checkbox" id="my_modal_7" class="modal-toggle" />
    <div class="modal" role="dialog">
        <div class="modal-box">
            <h3 class="text-lg font-bold">Delete & Move</h3>
            <p class="py-4">
                Chapter list should be displayed here and each chapter should be draggable. Delete button is here too.
                Maybe create dividers here.
            </p>
        </div>
        <label class="modal-backdrop" for="my_modal_7">Close</label>
    </div>
</template>


<style scoped>
</style>
