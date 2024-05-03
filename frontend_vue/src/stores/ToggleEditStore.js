import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useToggleEditStore = defineStore("toggleEditStore", () => {
    // ----- State -----
    const active_edit_course = ref('') // Id of the course being edited

    // ----- Getters -----

    // Returns true if course is being edited
    function isEditCourse(id) {
        return active_edit_course.value === id
    }


    // ----- Actions -----

    // Sets the course being edited
    function setEditCourse(id) {
        if (isEditCourse(id)) {
            active_edit_course.value = ''
        } else {
            active_edit_course.value = id
        }
    }


    return {
        active_edit_course,
        isEditCourse,
        setEditCourse
    }
})