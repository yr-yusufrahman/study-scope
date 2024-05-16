import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useCourseStore } from "./CourseStore";
import { useChapterStore } from "./ChapterStore";
import refresh from "@/components/helpers/refresh";

export const useCardStore = defineStore('cardStore', () => {

    const chapter = ref(null)
    const cards = ref([])
    const additions = ref([]) // New cards added
    const edits = ref([]) // Cards edited: {question, answer, order}
    const removals = ref([]) // Cards removed
  
    // Getters
    const currentChapter = computed(() => chapter.value)
    const currentCards = computed(() => cards.value)


    // Sets the current chapter
    function setChapter(chapter_id) {
        chapter.value = chapter_id
    }

    function setCards(cards_list) {
        cards.value = cards_list
    }

    // Get cards for the selected chapter
    function getCardsRequest() {
        // Get cards for the selected chapter
        const getCards =  async () => {
            let success = false
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
                success = true       
            } catch (error) {
                console.log("Error getting cards for chapter: ", error)
            }
            return success
        }

        let success = getCards()
        if (!success) {

            // Refresh token
            let refreshed = refresh()
            if (refreshed) {
                success = getCards()
            }
            else {
                // Failed to refresh token
                success = false
            }
        }
        return success
    }

    function clear() {
        chapter.value = null
        cards.value = []
        /*
        additions.value = []
        edits.value = []
        removals.value = []
        */
    }
  
    return { 
        chapter,
        currentChapter,
        currentCards,
        setChapter,
        getCardsRequest,
        clear
    }
  })