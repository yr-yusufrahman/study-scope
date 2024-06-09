import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import makeRequest from "@/components/helpers/requestFlow"
import refresh from "@/components/helpers/refresh"

export const useCourseStore = defineStore("courseStore", () => {

    const courses = ref([])
    const additions = ref([]) // New courses added
    const edits = ref([]) // Courses edited: {id, new_title}
    const removals = ref([]) // Courses removed
    

    // ----- Getters ----- try and use computed?
    const getCourses = computed(() => courses.value)

    // ----- Actions -----

    // Sets the list of courses
    function setCourses(courses_list) {
        courses.value = courses_list
    }

    // Adds new course to the list and keeps track of additions
    function addCourse(title) {
        let success = false
        // Check if course already exists
        if (!courses.value.find(course => course.title === title)) {
            // Give course a local id for editing
            const generateId = () => {
                let id = Math.floor(Math.random() * 1000);
                let exists = courses.value.find(course => course.id === id)
                while (exists) {
                    id = Math.floor(Math.random() * 1000);
                    exists = courses.value.find(course => course.id === id)
                }
                return id
            }
            let new_course = {id: generateId(), title: title}
            courses.value.push(new_course)
            additions.value.push(new_course)
            console.log("Course additions: ", additions.value)
            success = true
        }
        return success
    }

    // Edits course in the list
    function editCourse(id, new_title) {
        let success = false
        // Check if course exists
        if (!courses.value.find(course => course.title === new_title)) {
            // Check if course is new
            if (additions.value.find(course => course.id === id)) {
                additions.value.forEach((item, index) => {
                    if (item.id === id) {
                        additions.value[index].title = new_title
                    }
                })
            }

            // Check if course has been edited before
            else if (edits.value.find(course => course.id === id)) {
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
            success = true
            console.log("Course edits: ", edits.value)
        }
        return success
    }

    // Removes course from the list and keeps track of deletions
    function removeCourse(id) {
        // If course is new, remove it from additions
        if (additions.value.find(course => course.id === id)) {
            additions.value = additions.value.filter(course => course.id !== id)
        } else {
            removals.value.push({id: id})
        }
        // Remove course from edit list as it is going to be deleted
        edits.value = edits.value.filter(course => course.id !== id)
        courses.value = courses.value.filter(course => course.id !== id)
        console.log("Course removals: ", removals.value)
    }


    // ----- Requests -----

    function getCoursesRequestWorks() {
        // Get courses
        const getCourses =  async () => {
            let success = false
            try {
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}

                const response = await axios.get('http://127.0.0.1:8000/courses/get-courses', { headers })
                const data = await response.data
                setCourses(data?.courses)

                success = true       
            } catch (error) {
                console.log("Error getting courses: ")
            }
            return success
        }

        let success = getCourses()
        if (!success) {

            // Refresh token
            let refreshed = refresh()
            if (refreshed) {
                success = getCourses()
            }
            else {
                // Failed to refresh token
                success = false
            }
        }
        return success
    }

    function getCoursesRequest() {
        // Get courses
        const getCourses =  async () => {
            let success = false
            try {
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}

                const response = await axios.get('http://127.0.0.1:8000/courses/get-courses', { headers })
                const data = await response.data
                setCourses(data?.courses)

                success = true       
            } catch (error) {
                console.log("Error getting courses: ")
            }
            return success
        }

        let success = makeRequest(getCourses)
        return success
    }

    function saveCoursesRequest() {
        const additions_list = additions.value
        const edits_list = edits.value
        const removals_list = removals.value
    
        // If changes were made
        if (additions_list.length > 0 || edits_list.length > 0 || removals_list.length > 0) {

            // Save changes to courses
            const saveChanges =  async () => {
                let success = false
                try {
                    const token = localStorage.getItem('token')
                    const headers = {"Authorization": `Bearer ${token}`}
                    const body = { 
                        add: additions_list,
                        edit: edits_list,
                        remove: removals_list
                    }

                    await axios.post('http://127.0.0.1:8000/courses/change-courses', body, { headers })
                    success = true
                } catch (error) {
                    console.log("Error saving changes: ")
                }
                return success
            }

            // Request flow for saving changes and refreshing token
            let success = makeRequest(saveChanges)
            return success
        }
    }

    return {
        getCourses,
        additions,
        edits,
        removals,

        setCourses,
        addCourse,
        editCourse,
        removeCourse,

        getCoursesRequest,
        saveCoursesRequest
    }
})