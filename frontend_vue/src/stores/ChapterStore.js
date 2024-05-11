import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useCourseStore } from "./CourseStore";

export const useChapterStore = defineStore('chapterStore', () => {
    const courseStore = useCourseStore()

    const chapter = ref(null)
    const chapter_additions = ref([]) // New chapters added
    const chapter_edits = ref([]) // Chapters edited: {id, new_title}
    const chapter_removals = ref([]) // Chapters removed
  
    // Returns list of chapters for the selected course
    function selectedChapters() {
        let selected = Number(localStorage.getItem('selectedCourse'))
        
        if (!selected) return null
        else {
            let course = courseStore.courses?.find(course => course.id === selected)
            let course_chapters = course?.chapters
            return course_chapters
        }
    }
  
    // Add chapter to course
    function addChapter(new_title) {
        let success = false

        // Find the course to add chapter to
        const course_id = Number(localStorage.getItem('selectedCourse'))
        let course = courseStore.courses.find(course => course.id === course_id)

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
            courseStore.courses.forEach((course, index) => {
                if (course.id === course_id) {
                    courseStore.courses[index] = course
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
        let course = courseStore.courses.find(course => course.id === course_id)
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
            courseStore.courses.forEach((course, index) => {
                if (course.id === course_id) {
                    courseStore.courses[index] = course
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
        let course = courseStore.courses.find(course => course.id === course_id)

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
        courseStore.courses.forEach((course, index) => {
            if (course.id === course_id) {
                courseStore.courses[index] = course
            }
        })

        console.log("Chapter removals: ", chapter_removals.value)
    }
  
    return { 
        chapter,

        selectedChapters,
        addChapter,
        editChapter,
        removeChapter
    }
  })