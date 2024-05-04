import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useToggleEditStore = defineStore("toggleEditStore", () => {
    // ----- State -----
    const active_edit = ref('') // Id of the course being edited
    const active_edit_chapter = ref('') // Id of the chapter being edited

    // ----- Getters -----

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


    return {
        active_edit,
        isEdit,
        setEdit
    }
})