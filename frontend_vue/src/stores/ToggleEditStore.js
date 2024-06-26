import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useToggleEditStore = defineStore("toggleEditStore", () => {
    // ----- State -----
    const active_edit = ref('') // Id of the course being edited
    const deleting = ref(false) // True if course is being deleted
    const delete_modal = ref(false) // Type of modal to show


    // ----- Getters -----

    const getDeleting = computed(() => deleting.value)
    const getDeleteModal = computed(() => delete_modal.value)

    // Returns true if course is being edited
    function isEdit(id) {
        return active_edit.value === id
    }


    // ----- Actions -----

    // Sets the course being edited
    function setEdit(id) {
        if (isEdit(id)) {
            active_edit.value = ''
        } else {
            active_edit.value = id
        }
    }

    function clear() { active_edit.value = '' }

    function setDeleteModal(type, id) { 
        delete_modal.value = type
        deleting.value = id
    }

    return {
        active_edit,
        getDeleting,
        getDeleteModal,

        isEdit,
        setEdit,
        clear,
        setDeleteModal
    }
})