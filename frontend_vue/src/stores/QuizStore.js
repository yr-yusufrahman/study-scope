import { computed, ref } from "vue"
import { defineStore } from "pinia"
import axios from "axios"
import refresh from "@/components/helpers/refresh"
import { useCardStore } from "./CardStore"

export const useQuizStore = defineStore('quizStore', () => {
    const card_store = useCardStore()

    const loading = ref(true)
    const quiz = ref([])
    const history = ref([]) // History of the user's answers
    const location = ref(0) // Index of the current question
    const blank_index = ref(-1) // Index of the current blank word in the question
    const options = ref([]) // Options for the current blank word
    const mistakes = ref(0) // Number of mistakes made by the user
    const total = ref(0) // Total number of potential answers in the quiz
    const marks = ref(0)
    const reveal = ref(false)


    // Getters
    const getLoading = computed(() => loading.value)
    const getQuiz = computed(() => quiz.value)
    const getHistory = computed(() => history.value)
    const getTotal = computed(() => total.value)
    const getMarks = computed(() => marks.value)
    const getLocation = computed(() => location.value)
    const isMultipleChoice = computed(() => quiz.value[location.value]?.multiple_choice)
    const getQuestion = computed(() => quiz.value[location.value]?.question)
    const getAnswer = computed(() => quiz.value[location.value]?.answer)
    const getBlanks = computed(() => quiz.value[location.value]?.blanked)
    const getBlankAnswer = computed(() => quiz.value[location.value]?.blanked[blank_index.value])
    const getMistakes = computed(() => mistakes.value)
    const isAnswered = computed(() => history.value[location.value])
    const getReveal = computed(() => reveal.value)
    
    // MCQ Options for the current blank word
    const getOptions = computed(() => {
        if (blank_index.value !== -1) {
            return quiz.value[location.value]?.options[blank_index.value]
        }
        return []
    })


    // Setters
    function setLoading(loading_state) {
        loading.value = loading_state
    }

    function setQuiz(quiz_list) {
        quiz.value = quiz_list
    }

    function setHistory(history_list) {
        history.value = history_list
    }

    function setTotal(quiz_total) {
        total.value = quiz_total
    }

    function setMarks(mark) {
        marks.value = mark
    }

    function setLocation(location_state) {
        location.value = location_state
    }

    // Set the options for the current blank word
    function setOptions(index) {
        blank_index.value = index

        // Get the answer for the current blank word
        const answer = getBlankAnswer.value
    
        // Insert the answer into the options at a random index
        const option_list = getOptions.value
        if (option_list.length !== 4) {
            const insert_index = Math.floor(Math.random() * option_list.length+1)
            option_list.splice(insert_index, 0, answer)    
        }
        options.value = option_list
    }

    function clearOptions() {
        blank_index.value = -1
        options.value = []
    }

    function setMistakes(mistakes_state) {
        mistakes.value = mistakes_state
    }

    function endQuiz() {
        clearOptions()
        setMistakes(0)
        setTotal(0)
        setMarks(0)
        setLocation(0)
    }

    // Record the user's answer for a multiple choice question: -1 unanswered, 0 incorrect, 1 correct
    function recordMultipleChoiceAnswer(answer_type) {
        history.value[location.value][blank_index.value] = answer_type
    }

    function recordRateAnswer(answer) {
        history.value[location.value][0] = answer
    }

    function setReveal(reveal_state) {
        reveal.value = reveal_state
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

                setQuiz(data.quiz_content)
                setTotal(data.total)
                setHistory(data.history)
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

    function saveRevision() {}

    return {
        getLoading,
        getQuiz,
        getTotal,
        getMarks,
        getLocation,
        isMultipleChoice,
        getQuestion,
        getAnswer,
        getBlanks,
        getBlankAnswer,
        getOptions,
        getMistakes,
        getHistory,
        isAnswered,
        getReveal,

        setLoading,
        setMarks,
        setLocation,
        setOptions,
        clearOptions,
        setMistakes,
        endQuiz,
        recordMultipleChoiceAnswer,
        recordRateAnswer,
        setReveal,

        getQuizRequest
    }
})