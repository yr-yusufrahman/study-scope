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
    const getChapter = computed(() => chapter.value)
    const getCards = computed(() => cards.value)


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


    // Add card to chapter
    function addCard(new_question, new_answer, index) {

        // No need to check if card exists, user can add multiple cards with same question
        // Give card a local id for editing
        const generateId = () => {
            let id = Math.floor(Math.random() * 1000)
            let exists = cards.value.find(card => card.id === id)
            while (exists) {
                id = Math.floor(Math.random() * 1000)
                exists = cards.value.find(card => card.id === id)
            }
            return id
        }
        let new_card = {id: generateId(), question: new_question, answer: new_answer, order: index}

        // Add card to additions
        additions.value.push(new_card)

        // Update state by inserting card at correct index
        cards.value.splice(index, 0, new_card);
    }

    // Remove card from chapter
    function removeCard(id) {
        // Check if card is new
        if (additions.value.find(card => card.id === id)) {
            additions.value = additions.value.filter(card => card.id !== id)
        } else {
            removals.value.push(id)
        }

        // Remove from edits and Update state
        edits.value = edits.value.filter(card => card.id !== id)
        cards.value = cards.value.filter(card => card.id !== id)
    }

    // Edit card in chapter
    function editCard(id, new_question, new_answer) {
        // Check if card is new
        if (additions.value.find(card => card.id === id)) {
            additions.value.forEach((item, index) => {
                if (item.id === id) {
                    additions.value[index].question = new_question
                    additions.value[index].answer = new_answer
                }
            })
        } else if (edits.value.find(card => card.id === id)) {
            edits.value.forEach((item, index) => {
                if (item.id === id) {
                    edits.value[index].question = new_question
                    edits.value[index].answer = new_answer
                }
            })
        } else {
            edits.value.push({id, new_question, new_answer})
        }

        // Update state
        cards.value.forEach(card => {
            if (card.id === id) {
                card.question = new_question
                card.answer = new_answer
            }
        })
    }

    return { 
        chapter,
        getChapter,
        getCards,
        setChapter,
        getCardsRequest,
        clear,
        addCard,
        removeCard,
        editCard
    }
  })