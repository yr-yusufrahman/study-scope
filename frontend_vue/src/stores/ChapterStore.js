import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useCourseStore } from "./CourseStore";
import makeRequest from "@/components/helpers/requestFlow";

export const useChapterStore = defineStore('chapterStore', () => {

    const course = ref(-1) // Selected course, use this first then localStorage. localStorage is to persist data
    const chapters = ref([])
    const chapter_additions = ref([]) // New chapters added
    const chapter_edits = ref([]) // Chapters edited: {id, new_title}
    const chapter_removals = ref([]) // Chapters removed
  
    // Getters
    const getChapters = computed(() => chapters.value)



    // Setters

    // Sets all chapters for the selected course
    function setChapters(chapter_list) {
        chapters.value = chapter_list
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
            chapter_additions.value.push(new_chapter)

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
            if (chapter_additions.value.some(chapter => chapter.id === id)) {
                const add_index = chapter_additions.value.findIndex(chapter => chapter.id === id)
                chapter_additions.value[add_index].title = new_title
            }

            // Check if chapter has been edited before
            else if (chapter_edits.value.some(chapter => chapter.id === id)) {
                const edit_index = chapter_additions.value.findIndex(chapter => chapter.id === id)
                chapter_additions.value[edit_index].title = new_title

            } else {
                chapter_edits.value.push({id, new_title})
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
        const isNew = () => chapter_additions.value.some(chapter => chapter.id === id)
        if (isNew()) {
            chapter_additions.value = chapter_additions.value.filter(chapter => chapter.id !== id)
        } else {
            chapter_removals.value.push(id) // Using id to delete will work as the id is given by backend
        }

        // Remove course from edit list as it is going to be deleted
        chapter_edits.value = chapter_edits.value.filter(chapter => chapter.id !== id)
        
        // Update state
        chapters.value = chapters.value.filter(chapter => chapter.id !== id)
    }
  

    // Requests
    function getChaptersRequest() {
        // Get chapters
        const getChapters =  async () => {
            let success = false
            try {
                const selected_course = Number(localStorage.getItem('selectedCourse'))
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}
                const body = { 
                    course_id: selected_course,
                }

                const response = await axios.post('http://127.0.0.1:8000/courses/get-chapters', body, { headers })
                const data = await response.data
                setChapters(data?.chapters)

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


    return { 
        getChapters,

        addChapter,
        editChapter,
        removeChapter,

        getChaptersRequest
    }
  })