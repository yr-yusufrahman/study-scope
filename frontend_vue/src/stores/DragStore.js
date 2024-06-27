import { defineStore } from "pinia"
import { computed, ref } from "vue"
import { useChapterStore } from "./ChapterStore"
import { useCardStore } from "./CardStore"

export const useDragStore = defineStore('dragStore', () => {

    const chapter_store = useChapterStore()
    const card_store = useCardStore()

    // ----- State -----
    const dragging = ref(null)
    const drag_index = ref(null)
    const isScrolling = ref(false)
    const droppedCorrectly = ref(null)
    const update = ref(0)

    // ----- Getters -----
    const getDragging = computed(() => dragging.value)
    const getScrolling = computed(() => isScrolling.value)
    const getDroppedCorrectly = computed(() => droppedCorrectly.value)
    const getUpdate = computed(() => update.value)

    // ----- Actions -----
    function setDragging(id) { dragging.value = id }
    function setScrolling(state) { isScrolling.value = state }
    function setDroppedCorrectly(state) { droppedCorrectly.value = state }
    function setDragIndex(index) { drag_index.value = index }
    function setDropUpdate() { update.value += 1 }

    // Move card in state
    function setMoveCard() {
        const new_index = drag_index.value
        const id = dragging.value
        let force_update = false

        // Check if card is dragged and moved to a position
        if (id !== null && new_index !== null) {
            let cards = card_store.getCards

            // Get current index
            const current_index = cards.findIndex(card => card.id === id)

            // Check if card was moved
            if (current_index !== new_index) {
                const card = cards[current_index]

                // Remove card from current index and insert at new index - update state store only once
                let new_cards = cards.filter(card => card.id !== id)
                new_cards.splice(new_index, 0, card)

                // Update order of cards
                card_store.setCards(new_cards)
                card_store.setMoves(new_cards)

                force_update = true
            } else if (new_index === cards.length-1) {
                force_update = true
            }         
        }
        return force_update
    }

    // Move chapter in state
    function setMoveChapter() {
        const new_index = drag_index.value
        const id = dragging.value
        let force_update = false

        // Check if card is dragged and moved to a position
        if (id !== null && new_index !== null) {
            let items = chapter_store.getChapters

            // Get current index
            const current_index = items.findIndex(item => item.id === id)

            // Check if card was moved
            if (current_index !== new_index) {
                const card = items[current_index]

                // Remove card from current index and insert at new index - update state store only once
                let new_items = items.filter(item => item.id !== id)
                new_items.splice(new_index, 0, card)

                // Update order of cards
                chapter_store.setChapters(new_items)
                chapter_store.setMoves(new_items)
                console.log("New chapters: ", new_items)
                force_update = true
            } else if (new_index === items.length-1) {
                force_update = true
            }         
        }
        return force_update
    }

    // Clear drag state
    function clear() {
        dragging.value = null
        drag_index.value = null
        isScrolling.value = false
        droppedCorrectly.value = null
        update.value = 0
    }

    return {
        dragging,
        drag_index,
        isScrolling,
        droppedCorrectly,
        update,

        getDragging,
        getScrolling,
        getDroppedCorrectly,
        getUpdate,

        setDragging,
        setScrolling,
        setDroppedCorrectly,
        setDragIndex,
        setDropUpdate,
        setMoveCard,
        setMoveChapter,
        clear
    }
})
