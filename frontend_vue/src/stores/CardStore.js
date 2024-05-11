import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useCourseStore } from "./CourseStore";
import { useChapterStore } from "./ChapterStore";

export const useCardStore = defineStore('cardStore', () => {

    const chapter = ref(-1)
    const cards = ref([])
    const additions = ref([]) // New cards added
    const edits = ref([]) // Cards edited: {question, answer, order}
    const removals = ref([]) // Cards removed
  
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

    // Sets the current chapter
    function setChapter(chapter_id) {
        chapter.value = chapter_id
    }

    function setCards(cards_list) {
        cards.value = cards_list
    }

    // Get cards for the selected chapter
    const getCards =  async () => {
        try {
            const token = localStorage.getItem('token')
            const headers = {"Authorization": `Bearer ${token}`}
            const body = { 
                chapter_id: chapter.value
            }

            const response = await axios.post('http://127.0.0.1:8000/courses/cards', body, { headers })
            const data = await response.data
            console.log("Response in getCards in card store: ", data?.cards)
            setCards(data?.cards)
            return data?.cards            
        } catch (error) {
            console.log("Error getting cards for chapter: ", error)
            // Refresh token
            return false
        }
    }

  
    return { 
        chapter,

        setChapter,
        getCards,
        selectedChapters,

    }
  })