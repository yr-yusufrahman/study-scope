import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useCourseStore = defineStore("courseStore", () => {
    // ----- State -----
    const courses = ref([])
    const additions = ref([]) // New courses added
    const edits = ref([]) // Courses edited: {id, new_title}
    const removals = ref([]) // Courses removed

    // ----- Getters -----



    // ----- Actions -----

    // Sets the list of courses
    function setCourses(courses_list) {
        courses.value = courses_list
    }


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
            removals.value.push(id)
        }
        // Remove course from edit list as it is going to be deleted
        edits.value = edits.value.filter(course => course.id !== id)
        courses.value = courses.value.filter(course => course.id !== id)
        console.log("Deletions list: ", removals.value)
    }

    return {
        courses,
        additions,
        removals,
        setCourses,
        courseExists,
        addCourse,
        editCourse,
        removeCourse
    }
})