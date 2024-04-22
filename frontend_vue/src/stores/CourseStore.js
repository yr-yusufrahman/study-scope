import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useCourseStore = defineStore("courseStore", () => {
    // ----- State -----
    const courses = ref([])
    const additions = ref([]) // New courses added

    // ----- Getters -----



    // ----- Actions -----

    // Checks if course already exists in the list
    function courseExists(title) {
        return courses.value.find(course => course.title === title)
    }

    // Adds new course to the list and keeps track of additions
    function addCourse(new_course) {
        courses.value.push(new_course)
        additions.value.push(new_course)
    }   

    return {
        courses,
        additions,
        courseExists,
        addCourse
    }
})