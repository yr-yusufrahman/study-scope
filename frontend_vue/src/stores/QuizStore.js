import { computed, ref } from "vue"
import { defineStore } from "pinia"
import axios from "axios"
import refresh from "@/components/helpers/refresh"
import { useCardStore } from "./CardStore"

export const useQuizStore = defineStore('quizStore', () => {
    const card_store = useCardStore()

    const quiz = ref([])
    const loading = ref(true)


    // Getters
    const getQuiz = computed(() => quiz.value)
    const getLoading = computed(() => loading.value)


    // Setters
    function setQuiz(quiz_list) {
        quiz.value = quiz_list
    }

    function setLoading(loading_state) {
        loading.value = loading_state
    }


    // Request
    function getQuizRequest() {
        // Get the quiz for the selected chapter
        const getQuiz = async () => {
            let success = false
            try {
                const token = localStorage.getItem('token')
                const headers = {"Authorization": `Bearer ${token}`}
                const body = {
                    cards: card_store.getCards,
                    //chapter_id: card_store.getChapter
                }

                const response = await axios.post('http://127.0.0.1:8000/predictor/get-quiz', body, { headers })
                const data = await response.data
                console.log(data)
                setQuiz(data)
  
            } catch (error) {
                console.log("Error getting quiz for chapter: ")
            } finally {
                loading.value = false
            }
            return success
        }

        let success = getQuiz()
        if (!success) {

            // Refresh token
            let refreshed = refresh()
            if (refreshed) {
                success = getQuiz()
            }
            else {
                // Failed to refresh token
                success = false
            }
        }
        return success
    }

    return {
        getQuizRequest,
        getQuiz,
        getLoading,
        setLoading,
    }
})