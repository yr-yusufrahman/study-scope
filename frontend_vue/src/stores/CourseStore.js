import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import makeRequest from "@/components/helpers/requestFlow"
import equalStrings from "@/components/helpers/equalStrings"


export const useCourseStore = defineStore("courseStore", () => {
    let additions = [] // New courses added
    let edits = [] // Courses edited: {id, new_title}
    let removals = [] // Courses removed

    // ----- State -----
    const courses = ref([])
    const deleting = ref(false)
    const checkModified = ref(0)

    // ----- Getters ----- try and use computed?
    const getCourses = computed(() => courses.value)
    const getDeleting = computed(() => deleting.value)
    const isModified = computed(() => {
        checkModified.value += 1
        const edited = additions.length > 0 || edits.length > 0 || removals.length > 0
        return edited
    })

    // ----- Actions -----

    // Sets the list of courses
    function setCourses(courses_list) { courses.value = courses_list }

    // Adds new course to the list and keeps track of additions
    function addCourse(title) {
        let success = false
        // Check if course already exists
        if (!courses.value.find(course => equalStrings(course.title, title))) {
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

            // Keep alphabetical order of course titles
            courses.value.push(new_course);
            courses.value.sort((a, b) => a.title.localeCompare(b.title));

            additions.push(new_course)
            console.log("Course additions: ", additions)
            success = true
        }
        return success
    }

    // Edits course in the list
    function editCourse(id, new_title) {
        let success = false
        // Check if course exists
        if (!courses.value.find(course => equalStrings(course.title, new_title))) {
            // Check if course is new
            if (additions.find(course => course.id === id)) {
                additions.forEach((item, index) => {
                    if (item.id === id) {
                        additions[index].title = new_title
                    }
                })
            }

            // Check if course has been edited before
            else if (edits.find(course => course.id === id)) {
                edits.forEach((item, index) => {
                    if (item.id === id) {
                        edits[index].new_title = new_title
                    }
                })
            } else {
                edits.push({id, new_title})
            }

            // Update state
            courses.value.forEach(course => {
                if (course.id === id) {
                    course.title = new_title
                }
            })
            success = true
            console.log("Course edits: ", edits)
        }
        return success
    }

    // Removes course from the list and keeps track of deletions
    function removeCourse(id) {
        // If course is new, remove it from additions
        if (additions.find(course => course.id === id)) {
            additions = additions.filter(course => course.id !== id)
        } else {
            removals.push({id: id})
        }
        // Remove course from edit list as it is going to be deleted
        edits = edits.filter(course => course.id !== id)
        courses.value = courses.value.filter(course => course.id !== id)
        console.log("Course removals: ", removals)
    }

    function setDeleting(state) { deleting.value = state }

    // ----- Requests -----

    function getCoursesRequest() {
        // Get courses
        const getCourses =  async () => {
            let success = false
            try {
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}

                const response = await axios.get('http://127.0.0.1:8000/courses/get-courses', { headers })
                const data = await response.data
                setCourses(data?.courses ?? [])

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
        const edited = additions.length > 0 || edits.length > 0 || removals.length > 0
        // If changes were made
        if (edited) {

            // Save changes to courses
            const saveChanges =  async () => {
                let success = false
                try {
                    const token = localStorage.getItem('token')
                    const headers = {"Authorization": `Bearer ${token}`}
                    const body = { 
                        add: additions,
                        edit: edits,
                        remove: removals
                    }

                    await axios.post('http://127.0.0.1:8000/courses/change-courses', body, { headers })
                    // Clear changes
                    additions = []
                    edits = []
                    removals = []
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



    // Testing predictor tree request
    function treeRequest() {
        // Get courses
        const getTree =  async () => {
            let success = false
            try {
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}

                const response = await axios.get('http://127.0.0.1:8000/predictor/get-tree', { headers })
                const data = await response.data
                //setCourses(data?.courses)

                success = true       
            } catch (error) {
                console.log("Error getting tree: ")
            }
            return success
        }

        let success = makeRequest(getTree)
        return success
    }

    return {
        courses,
        deleting,
        checkModified,

        getCourses,
        getDeleting,
        isModified,

        setCourses,
        addCourse,
        editCourse,
        removeCourse,
        setDeleting,

        getCoursesRequest,
        saveCoursesRequest,

        // Testing predictor tree request
        treeRequest
    }
})