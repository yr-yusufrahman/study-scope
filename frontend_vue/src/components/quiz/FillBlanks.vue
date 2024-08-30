<script setup>
import { ref, onBeforeUpdate, onMounted } from 'vue'
import { useQuizStore } from '@/stores/QuizStore'


const quiz_store = useQuizStore()

const blanked_answer = ref([])
const reload = ref(0)

onBeforeUpdate(() => {
	if (quiz_store.getType === 1) {
		blanked_answer.value = splitTextIntoParts()
		reload.value = quiz_store.getHistory.length
	}
})


// Split the answer into parts to distinguish between blanked words and other text
function splitTextIntoParts() {
	let parts = []
	let remaining_string = quiz_store.getAnswer
	let wordsToBlank = quiz_store.getBlanks

	// Examine each word to be blanked
	wordsToBlank?.forEach((word, index) => {
		const formatted_string = remaining_string.toLowerCase()
		const wordIndex = formatted_string.indexOf(word)

		// If the word is found in the answer string
		if (wordIndex !== -1) {
			// Add the text before the word
			if (wordIndex > 0) {
				parts.push({ text: remaining_string.substring(0, wordIndex), isWord: false })
			}

			// Add the blanked word
			parts.push({ text: word, isWord: true, index: index})
			remaining_string = remaining_string.substring(wordIndex + word.length)
		}
	})

	// Add the remaining text after the last blanked word
	if (remaining_string.length > 0) {
		parts.push({ text: remaining_string, isWord: false })
	}

	return parts
}


// Checks if two strings are roughly equal. calculates number of character edits to change one string to another
function roughEqualStrings(a, b) {
  const matrix = [];

  // Create an empty 2D array
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = new Array(a.length + 1).fill(0);
  }

  // Initialize the first row and column of the matrix
  for (let i = 0; i <= a.length; i++) {
    matrix[0][i] = i;
  }
  for (let i = 0; i <= b.length; i++) {
    matrix[i][0] = i;
  }

  // Populate the matrix with the Levenshtein distance values
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1, // Substitution
          matrix[i - 1][j] + 1, // Deletion
          matrix[i][j - 1] + 1 // Insertion
        );
      }
    }
  }

	const distance = matrix[b.length][a.length]
  return distance <= 2
}


// Input answer for the blanked word
function inputAnswer(blank_index, word_index, event) {
	const answer = blanked_answer.value[word_index].text.toLowerCase()
	const input = event.target.value.trim().toLowerCase()

	if (roughEqualStrings(input, answer)) {
		quiz_store.setBlankIndex(blank_index)
		quiz_store.setMarks(quiz_store.getMarks + 1)
		quiz_store.recordChoiceAnswer(1)
		quiz_store.setBlankIndex(-1)
	}
}


// Reveals all the answers
function showAnswers() {
	const all_blanks = quiz_store.getBlanks
	all_blanks.forEach((blank, index) => {
		const answred = quiz_store.isAnswered[index]
		if (answred === -1) {
			quiz_store.setBlankIndex(index)
			quiz_store.setMistakes(quiz_store.getMistakes + 1)
			quiz_store.setMarks(quiz_store.getMarks + 1)
			quiz_store.recordChoiceAnswer(0)			
		}
	})
	quiz_store.setBlankIndex(-1)
}
</script>


<template>
	<div class="h-full w-full flex flex-col items-center justify-center gap-6">
		<h1>Fill-in blanks is very similar to MCQ. Replace blanked word buttons with text inputs</h1>
		<!-- Multiple choice blanked answer -->
		<div v-show="quiz_store.getType === 1" class="w-4/5" >
			<p v-if="!quiz_store.isAnswered"></p>
			<p v-else>
				<span v-for="(part, index) in blanked_answer" :key="index">
					<span v-if="part.isWord">

						<!-- If blanked word is answered -->
						<span v-if="quiz_store.isAnswered[part.index] === 1" class="blue">{{ part.text }}</span> 
						
						<!-- If all options were attempted -->
						<span v-else-if="quiz_store.isAnswered[part.index] === 0" class="pastel-red">{{ part.text }}</span>


						<input v-else
							type="text"
							placeholder="One word"
							class="input input-bordered input-info input-sm w-full max-w-xs blue"
							@keyup="inputAnswer(part.index, index, $event)"
						/>

					</span>
					<span v-else>{{ part.text }}</span>
				</span>
			</p>

		</div>

		<!-- Show answers -->
		 <button v-show="!quiz_store.allChoicesAnswered" class="btn btn-error" @click="showAnswers">Show answers</button>
  </div>
</template>


<style scoped>
</style>
