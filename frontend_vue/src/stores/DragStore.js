import { defineStore } from "pinia"
import { computed, ref } from "vue"
import { useChapterStore } from "./ChapterStore"
import { useCardStore } from "./CardStore"

export const useDragStore = defineStore('dragStore', () => {
    const card_store = useCardStore()
    const cards = ref(card_store.getCards)
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
            // Get current index
            const current_index = cards.value.findIndex(card => card.id === id)

            // Check if card was moved
            if (current_index !== new_index) {
                const card = cards.value[current_index]

                // Remove card from current index and insert at new index - update state store only once
                let new_cards = cards.value.filter(card => card.id !== id)
                new_cards.splice(new_index, 0, card)
                cards.value = new_cards

                // Update order of cards
                card_store.setCards(new_cards)
                card_store.setMoves(new_cards)

                force_update = true
            } else if (new_index === cards.value.length-1) {
                force_update = true
            }         
        }
        return force_update
    }

    return {
        getDragging,
        getScrolling,
        getDroppedCorrectly,
        getUpdate,
        
        setDragging,
        setScrolling,
        setDroppedCorrectly,
        setDragIndex,
        setDropUpdate,
        setMoveCard
    }
})
