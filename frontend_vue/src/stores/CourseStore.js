import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useCourseStore = defineStore("courseStore", () => {
    // ----- State -----
    const courses = ref([])
    const additions = ref([]) // New courses added
    const edits = ref([]) // Courses edited: {id, new_title}
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

    // Edits course in the list
    function editCourse(id, new_title) {
        // Check if course has been edited before
        if (edits.value.find(course => course.id === id)) {
            edits.value.forEach((item, index) => {
                if (item.id === id) {
                    edits.value[index].new_title = new_title
                }
            })
        } else {
            edits.value.push({id, new_title})
        }
        // Update state
        courses.value.forEach(course => {
            if (course.id === id) {
                course.title = new_title
            }
        })
        console.log("Edits list: ", edits.value)
    }

    // Removes course from the list and keeps track of deletions
    function removeCourse(id) {
        // If course is new, remove it from additions
        if (additions.value.find(course => course.id === id)) {
            additions.value = additions.value.filter(course => course.id !== id)
        } else {
            deletions.value.push(id)
        }
        courses.value = courses.value.filter(course => course.id !== id)
        console.log("Deletions list: ", deletions.value)
    }

    return {
        courses,
        additions,
        deletions,
        courseExists,
        addCourse,
        editCourse,
        removeCourse
    }
})