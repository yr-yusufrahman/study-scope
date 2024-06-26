import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import makeRequest from "@/components/helpers/requestFlow";
import { useChapterStore } from "./ChapterStore";

export const useCardStore = defineStore('cardStore', () => {
    const chapter = ref(null)
    const chapter_name = ref('')
    const due = ref(null)

    const cards = ref([])
    const additions = ref([]) // New cards added
    const edits = ref([]) // Cards edited: {question, answer, order}
    const removals = ref([]) // ID of cards removed
    const moves = ref([]) // Cards moved: Use ID and new index like {id, new_index} or store list of ID representing new order

  
    // Getters
    const getChapter = computed(() => chapter.value)
    const getChapterName = computed(() => chapter_name.value)
    const getDue = computed(() => due.value)
    const getCards = computed(() => cards.value)



    // Sets the current chapter
    function setChapter(id) {
        chapter.value = id
        localStorage.setItem('selectedChapter', id)
    }

    // Clears the current chapter
    function clear() {
        chapter.value = null
        chapter_name.value = ''
        cards.value = []

        localStorage.removeItem('selectedChapter')
        /*
        additions.value = []
        edits.value = []
        removals.value = []
        */
    }    

    function setCards(cards_list) { cards.value = cards_list }

    function setMoves(cards_list) { moves.value = cards_list.map(card => card.id) }

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

        // Update order of cards
        setMoves(cards.value)
    }

    // Remove card from chapter
    function removeCard(id) {
        // Check if card is new
        if (additions.value.find(card => card.id === id)) {
            additions.value = additions.value.filter(card => card.id !== id)
        } else {
            removals.value.push({id: id})
        }

        // Remove from edits and Update state
        edits.value = edits.value.filter(card => card.id !== id)
        cards.value = cards.value.filter(card => card.id !== id)

        // Update order of cards
        setMoves(cards.value)
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


    // ----- Requests -----
    
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

                const response = await axios.post('http://127.0.0.1:8000/courses/get-cards', body, { headers })
                const data = await response.data

                setCards(data?.cards)
                chapter_name.value = data?.chapter_title
                due.value = data?.next_due

                success = true       
            } catch (error) {
                console.log("Error getting cards for chapter: ")
            }
            return success
        }

        let success = makeRequest(getCards)
        return success
    }

    function saveCardsRequest() {
        const additions_list = additions.value
        const edits_list = edits.value
        const removals_list = removals.value
        const moves_list = moves.value
    
        // If changes were made
        if (additions_list.length > 0 || edits_list.length > 0 || removals_list.length > 0 || moves_list.length > 0) {

            // Save changes to courses
            const saveChanges =  async () => {
                let success = false
                try {
                    const chapter_id = chapter.value
                    const token = localStorage.getItem('token')
                    const headers = {"Authorization": `Bearer ${token}`}
                    const body = { 
                        add: additions_list,
                        edit: edits_list,
                        remove: removals_list,
                        move: moves_list,
                        chapter_id: chapter_id
                    }

                    await axios.post('http://127.0.0.1:8000/courses/change-cards', body, { headers })
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
        getChapter,
        getChapterName,
        getDue,
        getCards,

        setChapter,
        clear,
        setCards,
        setMoves,
        addCard,
        removeCard,
        editCard,

        getCardsRequest,
        saveCardsRequest
    }
  })