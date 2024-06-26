import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useCourseStore } from "./CourseStore";
import makeRequest from "@/components/helpers/requestFlow";

export const useChapterStore = defineStore('chapterStore', () => {

    const course = ref(-1) // Selected course, use this first then localStorage. localStorage is to persist data
    const course_name = ref('')
    const chapters = ref([])
    const additions = ref([]) // New chapters added
    const edits = ref([]) // Chapters edited: {id, new_title}
    const removals = ref([]) // Chapters removed
  
    // Getters
    const getCourse = computed(() => course.value)
    const getCourseName = computed(() => course_name.value)
    const getChapters = computed(() => chapters.value)



    // Setters

    // Sets all chapters for the selected course
    function setChapters(chapter_list) { chapters.value = chapter_list }

    function selectCourse(id) {
        localStorage.setItem('selectedCourse', id)
        course.value = id
    }

    // Add chapter to course
    function addChapter(new_title) {
        let success = false

        // Check if chapter exists
        const exists = () => chapters.value.find(chapter => chapter.title === new_title)
        if (!exists()) {
            
            // Give chapter a local id for editing
            const generateId = () => {
                let id = Math.floor(Math.random() * 1000)
                let exists = chapters.value.find(chapter => chapter.id === id)
                while (exists) {
                    id = Math.floor(Math.random() * 1000)
                    exists = chapters.value.find(chapter => chapter.id === id)
                }
                return id
            }
            let new_chapter = {id: generateId(), title: new_title}

            // Add to chapter additions
            additions.value.push(new_chapter)

            // Update state
            chapters.value.push(new_chapter) 
            success = true        
        }
        return success
    }

    // Rename chapter
    function editChapter(id, new_title) {
        let success = false

        // Check if chapter exists with the new title
        const exists = () => chapters.value.some(chapter => chapter.title === new_title)
        if (!exists()) {

            // Check if chapter is new
            if (additions.value.some(chapter => chapter.id === id)) {
                const add_index = additions.value.findIndex(chapter => chapter.id === id)
                additions.value[add_index].title = new_title
            }

            // Check if chapter has been edited before
            else if (edits.value.some(chapter => chapter.id === id)) {
                const edit_index = additions.value.findIndex(chapter => chapter.id === id)
                additions.value[edit_index].title = new_title

            } else {
                edits.value.push({id, new_title})
            }

            // Update state
            const index = chapters.value.findIndex(chapter => chapter.id === id)
            chapters.value[index].title = new_title

            success = true
        }
        return success
    }

    // Remove chapter
    function removeChapter(id) {

        // If chapter is new, remove it from additions
        const isNew = () => additions.value.some(chapter => chapter.id === id)
        if (isNew()) {
            additions.value = additions.value.filter(chapter => chapter.id !== id)
        } else {
            removals.value.push({id: id}) // Using id to delete will work as the id is given by backend
        }

        // Remove course from edit list as it is going to be deleted
        edits.value = edits.value.filter(chapter => chapter.id !== id)
        
        // Update state
        chapters.value = chapters.value.filter(chapter => chapter.id !== id)
    }
  

    // Requests
    function getChaptersRequest() {
        // Get chapters
        const getChapters =  async () => {
            let success = false
            try {
                //const selected_course = Number(localStorage.getItem('selectedCourse'))
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}
                const body = { 
                    course_id: course.value,
                }

                const response = await axios.post('http://127.0.0.1:8000/courses/get-chapters', body, { headers })
                const data = await response.data
                setChapters(data?.chapters)
                course_name.value = data?.course_title

                success = true       
            } catch (error) {
                console.log("Error getting chapters: ")
            } finally {
                return success
            }   
        }

        // Request flow for getting courses and refreshing token
        let success = makeRequest(getChapters)
        return success
    }

    function saveChaptersRequest() {
        const additions_list = additions.value
        const edits_list = edits.value
        const removals_list = removals.value
        //const moves_list = moves.value
    
        // If changes were made
        if (additions_list.length > 0 || edits_list.length > 0 || removals_list.length > 0) {

            // Save changes to courses
            const saveChanges =  async () => {
                let success = false
                try {
                    const course_id = Number(localStorage.getItem('selectedCourse'))
                    const token = localStorage.getItem('token')
                    const headers = {"Authorization": `Bearer ${token}`}
                    const body = { 
                        add: additions_list,
                        edit: edits_list,
                        remove: removals_list,
                        //move: moves_list,
                        course_id: course_id
                    }

                    await axios.post('http://127.0.0.1:8000/courses/change-chapters', body, { headers })
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
        getCourse,
        getCourseName,
        getChapters,

        selectCourse,
        addChapter,
        editChapter,
        removeChapter,

        getChaptersRequest,
        saveChaptersRequest
    }
  })