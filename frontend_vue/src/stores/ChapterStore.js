import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useCourseStore } from "./CourseStore";
import makeRequest from "@/components/helpers/requestFlow";
import equalStrings from "@/components/helpers/equalStrings";


export const useChapterStore = defineStore('chapterStore', () => {

    let additions = [] // New chapters added
    let edits = [] // Chapters edited: {id, new_title}
    let removals = [] // Chapters removed
    let moves = []
    let initial_order = []
    let change_course = {
        id: [],
        new_course_id: null
    } // Chapter will be moved to another course: {id, new_course_id}

    // ----- State -----
    const course = ref(null) // Selected course, use this first then localStorage. localStorage is to persist data
    const course_name = ref('')
    const chapters = ref([])
    const checkModified = ref(0)
  
    // ----- Getters -----
    const getCourse = computed(() => course.value)
    const getCourseName = computed(() => course_name.value)
    const getChapters = computed(() => chapters.value)
    const isModified = computed(() => {
        checkModified.value += 1
        const edited = additions.length > 0 || edits.length > 0 || removals.length > 0
        const swapped = moves.length > 0 && changedOrder()
        const changed_course = change_course.new_course_id !== null
        return edited || swapped || changed_course
    })

    // ----- Actions -----

    // Sets all chapters for the selected course
    function selectCourse(id) {
        localStorage.setItem('selectedCourse', id)
        course.value = id
    }

    // Add chapter to course
    function addChapter(new_title) {
        let success = false

        // Check if chapter exists
        const exists = () => chapters.value.find(chapter => equalStrings(chapter.title, new_title))
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
            additions.push(new_chapter)

            // Update state
            chapters.value.push(new_chapter)
            setMoves(chapters.value)
            success = true        
        }
        return success
    }

    // Rename chapter
    function editChapter(id, new_title) {
        let success = false

        // Check if chapter exists with the new title
        const exists = () => chapters.value.some(chapter => equalStrings(chapter.title, new_title))
        if (!exists()) {

            // Check if chapter is new
            if (additions.some(chapter => chapter.id === id)) {
                const add_index = additions.findIndex(chapter => chapter.id === id)
                additions[add_index].title = new_title
            }

            // Check if chapter has been edited before
            else if (edits.some(chapter => chapter.id === id)) {
                const edit_index = additions.findIndex(chapter => chapter.id === id)
                additions[edit_index].title = new_title

            } else {
                edits.push({id, new_title})
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
        const isNew = () => additions.some(chapter => chapter.id === id)
        if (isNew()) {
            additions = additions.filter(chapter => chapter.id !== id)
        } else {
            removals.push({id: id}) // Using id to delete will work as the id is given by backend
        }

        // Remove course from edit list as it is going to be deleted
        edits = edits.filter(chapter => chapter.id !== id)
        
        // Update state
        chapters.value = chapters.value.filter(chapter => chapter.id !== id)
        setMoves(chapters.value)
    }

    // Change chapter course
    function changeChapterCourse(id_list, new_course_id) {
        chapters.value = chapters.value.filter(chapter => !id_list.includes(chapter.id))
        change_course.id = id_list
        change_course.new_course_id = new_course_id
        setMoves(chapters.value)
    }

    function setChapters(list) { chapters.value = list }

    function setMoves(list) { moves = list.map(chapter => chapter.id) }
    function setInitialOrder(list) { initial_order = list.map(chapter => chapter.id) }
    function changedOrder() { return JSON.stringify(initial_order) !== JSON.stringify(moves) }
  

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
                //setChapters(data?.chapters)
                chapters.value = data?.chapters
                course_name.value = data?.course_title
                setInitialOrder(data?.chapters) // Set initial order for reordering

                success = true 
            } catch (error) {
                console.log("Error getting chapters: ")
            }
            return success   
        }

        // Request flow for getting courses and refreshing token
        let success = makeRequest(getChapters)
        return success
    }

    function saveChaptersRequest() {
        const edited = additions.length > 0 || edits.length > 0 || removals.length > 0 || change_course.new_course_id !== null
        const swapped = moves.length > 0 && changedOrder()
    
        // If changes were made
        if (edited || swapped) {

            // Save changes to courses
            const saveChanges =  async () => {
                let success = false
                try {
                    const course_id = Number(localStorage.getItem('selectedCourse'))
                    const token = localStorage.getItem('token')
                    const headers = {"Authorization": `Bearer ${token}`}
                    const body = { 
                        add: additions,
                        edit: edits,
                        remove: removals,
                        move: moves,
                        switch: change_course,
                        course_id: course_id
                    }
                    await axios.post('http://127.0.0.1:8000/courses/change-chapters', body, { headers })
                    // Clear changes
                    additions = []
                    edits = []
                    removals = []
                    moves = []
                    change_course = {
                        id: [],
                        new_course_id: null
                    }
                    initial_order = []
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
        course,
        course_name,
        chapters,
        checkModified,

        getCourse,
        getCourseName,
        getChapters,
        isModified,

        selectCourse,
        addChapter,
        editChapter,
        removeChapter,
        changeChapterCourse,
        setChapters,
        setMoves,

        getChaptersRequest,
        saveChaptersRequest
    }
  })