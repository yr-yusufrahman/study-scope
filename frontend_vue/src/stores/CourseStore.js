import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useCourseStore = defineStore("courseStore", () => {
    // ----- State -----
    const courses = ref([])
    const additions = ref([]) // New courses added
    const edits = ref([]) // Courses edited: {id, new_title}
    const removals = ref([]) // Courses removed
    
    const chapter_additions = ref([]) // New chapters added
    const chapter_edits = ref([]) // Chapters edited: {id, new_title}
    const chapter_removals = ref([]) // Chapters removed

    // ----- Getters ----- try and use computed?

    // Returns list of chapters for the selected course
    function selectedChapters() {
        let selected = Number(localStorage.getItem('selectedCourse'))
        
        if (!selected) return null
        else {
            let course = courses.value.find(course => course.id === selected)
            let chapters = course?.chapters
            return chapters
        }
    }


    // ----- Actions -----

    // Get courses
    const getCourses =  async () => {
        try {
            const token = localStorage.getItem('token')
            const headers = {"Authorization": `Bearer ${token}`}

            const response = await axios.get('http://127.0.0.1:8000/courses/get', { headers })
            const data = await response.data
            setCourses(data?.courses)
            return true            
        } catch (error) {
            console.log("Error getting courses: ", error)
            // Refresh token
            return false
        }
    }


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
            removals.value.push(id)
        }
        // Remove course from edit list as it is going to be deleted
        edits.value = edits.value.filter(course => course.id !== id)
        courses.value = courses.value.filter(course => course.id !== id)
        console.log("Course removals: ", removals.value)
    }

    // Add chapter to course
    function addChapter(new_title) {
        let success = false

        // Find the course to add chapter to
        const course_id = Number(localStorage.getItem('selectedCourse'))
        let course = courses.value.find(course => course.id === course_id)

        // Check if chapter exists
        const exists = () => course?.chapters?.find(chapter => chapter.title === new_title)
        if (!exists()) {
            
            // Give chapter a local id for editing
            const generateId = () => {
                let id = Math.floor(Math.random() * 1000)
                let exists = course.chapters.find(chapter => chapter.id === id)
                while (exists) {
                    id = Math.floor(Math.random() * 1000)
                    exists = course.find(chapter => chapter.id === id)
                }
                return id
            }
            let new_chapter = {id: generateId(), title: new_title}

            // Add chapter to course state
            course.chapters.push(new_chapter)

            // Add to chapter additions
            chapter_additions.value.push(new_chapter)

            // Update state
            courses.value.forEach((course, index) => {
                if (course.id === course_id) {
                    courses.value[index] = course
                }
            })
            console.log("Chapter additions: ", chapter_additions.value)    
            success = true        
        }
        return success
    }

    // Rename chapter
    function editChapter(id, new_title) {
        let success = false
        const course_id = Number(localStorage.getItem('selectedCourse'))
        let course = courses.value.find(course => course.id === course_id)
        console.log("chapter id: ", id, "new title: ", new_title)
        // Check if chapter exists with the new title
        const exists = () => course?.chapters?.some(chapter => chapter.title === new_title)
        if (!exists()) {
            // Check if chapter is new
            if (chapter_additions.value.some(chapter => chapter.id === id)) {
                chapter_additions.value.forEach((item, index) => {
                    if (item.id === id) {
                        chapter_additions.value[index].title = new_title
                    }
                })
            }

            // Check if chapter has been edited before
            else if (chapter_edits.value.some(chapter => chapter.id === id)) {
                chapter_edits.value.forEach((item, index) => {
                    if (item.id === id) {
                        chapter_edits.value[index].new_title = new_title
                    }
                })
            } else {
                chapter_edits.value.push({id, new_title})
            }

            // Change title
            course.chapters.forEach(chapter => {
                if (chapter.id === id) {
                    chapter.title = new_title
                }
            })

            // Update state
            courses.value.forEach((course, index) => {
                if (course.id === course_id) {
                    courses.value[index] = course
                }
            })
            success = true
            console.log("Chapter edits: ", chapter_edits.value)
        }
        return success
    }

    // Remove chapter
    function removeChapter(id) {
        const course_id = Number(localStorage.getItem('selectedCourse'))
        let course = courses.value.find(course => course.id === course_id)

        // If chapter is new, remove it from additions
        const isNew = () => chapter_additions.value.some(chapter => chapter.id === id)
        if (isNew()) {
            chapter_additions.value = chapter_additions.value.filter(chapter => chapter.id !== id)
        } else {
            chapter_removals.value.push(id) // Using id to delete will work as the id is given by backend
        }

        // Remove course from edit list as it is going to be deleted
        chapter_edits.value = chapter_edits.value.filter(chapter => chapter.id !== id)
        course.chapters = course.chapters.filter(chapter => chapter.id !== id)

        // Update state
        courses.value.forEach((course, index) => {
            if (course.id === course_id) {
                courses.value[index] = course
            }
        })

        console.log("Chapter removals: ", chapter_removals.value)
    }

    return {
        courses,
        additions,
        edits,
        removals,

        getCourses,
        selectedChapters,

        setCourses,
        addCourse,
        editCourse,
        removeCourse,
        addChapter,
        editChapter,
        removeChapter
    }
})