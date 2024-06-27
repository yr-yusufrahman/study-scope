import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import makeRequest from "@/components/helpers/requestFlow";
import { useChapterStore } from "./ChapterStore";

export const useCardStore = defineStore('cardStore', () => {

    let additions = [] // New cards added
    let edits = [] // Cards edited: {question, answer, order}
    let removals = [] // ID of cards removed
    let moves = [] // Cards moved: Use ID and new index like {id, new_index} or store list of ID representing new order   
    let initial_order = [] // Initial order of cards

    // ----- State -----
    const chapter = ref(null)
    const chapter_name = ref('')
    const due = ref(null)
    const cards = ref([])
  
    // ----- Getters -----
    const getChapter = computed(() => chapter.value)
    const getChapterName = computed(() => chapter_name.value)
    const getDue = computed(() => due.value)
    const getCards = computed(() => cards.value)


    // ----- Actions
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

    function setMoves(cards_list) { moves = cards_list.map(card => card.id) }
    function setInitialOrder(list) { initial_order = list.map(card => card.id) }
    function changedOrder() { return JSON.stringify(initial_order) !== JSON.stringify(moves) }

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
        additions.push(new_card)

        // Update state by inserting card at correct index
        cards.value.splice(index, 0, new_card);

        // Update order of cards
        setMoves(cards.value)
    }

    // Remove card from chapter
    function removeCard(id) {
        // Check if card is new
        if (additions.find(card => card.id === id)) {
            additions = additions.filter(card => card.id !== id)
        } else {
            removals.push({id: id})
        }

        // Remove from edits and Update state
        edits = edits.filter(card => card.id !== id)
        cards.value = cards.value.filter(card => card.id !== id)

        // Update order of cards
        setMoves(cards.value)
    }

    // Edit card in chapter
    function editCard(id, new_question, new_answer) {
        // Check if card is new
        if (additions.find(card => card.id === id)) {
            additions.forEach((item, index) => {
                if (item.id === id) {
                    additions[index].question = new_question
                    additions[index].answer = new_answer
                }
            })
        } else if (edits.find(card => card.id === id)) {
            edits.forEach((item, index) => {
                if (item.id === id) {
                    edits[index].question = new_question
                    edits[index].answer = new_answer
                }
            })
        } else {
            edits.push({id, new_question, new_answer})
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

                cards.value = data?.cards
                chapter_name.value = data?.chapter_title
                due.value = data?.next_due
                setInitialOrder(data?.cards)

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
        const edited = additions.length > 0 || edits.length > 0 || removals.length > 0
        const swapped = moves.length > 0 && changedOrder()
        // If changes were made
        if (edited || swapped) {
            console.log("Saving changes")
            console.log("Edits: ", edits)

            // Save changes to courses
            const saveChanges =  async () => {
                let success = false
                try {
                    const chapter_id = chapter.value
                    const token = localStorage.getItem('token')
                    const headers = {"Authorization": `Bearer ${token}`}
                    const body = { 
                        add: additions,
                        edit: edits,
                        remove: removals,
                        move: moves,
                        chapter_id: chapter_id
                    }

                    await axios.post('http://127.0.0.1:8000/courses/change-cards', body, { headers })
                    // Clear changes
                    additions = []
                    edits = []
                    removals = []
                    moves = []
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
        chapter,
        chapter_name,
        due,
        cards,

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