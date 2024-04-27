import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useCourseStore = defineStore("courseStore", () => {
    // ----- State -----
    const courses = ref([])
    const additions = ref([]) // New courses added
    const deletions = ref([]) // Courses removed

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

    // Removes course from the list and keeps track of deletions
    function removeCourse(title) {
        // If course is new, remove it from additions
        if (additions.value.find(course => course.title === title)) {
            additions.value = additions.value.filter(course => course.title !== title)
        } else {
            deletions.value.push(title)
        }
        courses.value = courses.value.filter(course => course.title !== title)
        console.log(deletions.value)
    }

    return {
        courses,
        additions,
        deletions,
        courseExists,
        addCourse,
        removeCourse
    }
})