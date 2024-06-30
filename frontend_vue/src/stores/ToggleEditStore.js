import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useToggleEditStore = defineStore("toggleEditStore", () => {
    // ----- State -----
    const active_edit = ref('') // Id of the course being edited
    const deleting = ref(false) // True if course is being deleted
    const delete_modal = ref(false) // Type of modal to show
    const save_modal = ref(false) // True if save modal is open
    const redirect = ref(false) // True if redirect is needed


    // ----- Getters -----
    const getDeleting = computed(() => deleting.value)
    const getDeleteModal = computed(() => delete_modal.value)
    const getSaveModal = computed(() => save_modal.value)
    const getRedirect = computed(() => redirect.value)

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

    function setSaveModal(type) { save_modal.value = type }

    function clearModal() {
        delete_modal.value = false
        save_modal.value = false
    }

    function setRedirect(url) { redirect.value = url }

    return {
        active_edit,
        deleting,
        delete_modal,
        save_modal,

        getDeleting,
        getDeleteModal,
        getSaveModal,
        getRedirect,

        isEdit,
        setEdit,
        clear,
        setDeleteModal,
        setSaveModal,
        clearModal,
        setRedirect
    }
})