<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Navbar from '@/components/structure/Navbar.vue'
import { useChapterStore } from '@/stores/ChapterStore'
import { useCardStore } from '@/stores/CardStore'

const router = useRouter()
const chapterStore = useChapterStore()
const cardStore = useCardStore()
const starting = ref(false)
const error = ref('')

async function startSampleQuiz() {
  starting.value = true
  error.value = ''
  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
  try {
    const courses = (await axios.get('http://127.0.0.1:8000/courses/get-courses', { headers })).data?.courses ?? []
    const maths = courses.find((course) => course.title.toLowerCase() === 'maths')
    if (!maths) throw new Error('The Maths course is not in this account.')

    chapterStore.selectCourse(maths.id)
    const loaded = await chapterStore.getChaptersRequest()
    if (!loaded) throw new Error('Could not load the Maths chapters.')

    const differentiation = chapterStore.getChapters.find((chapter) => chapter.title.toLowerCase() === 'differentiation')
    if (!differentiation) throw new Error('Differentiation is not in the Maths course.')

    cardStore.setChapter(differentiation.id)
    const cardsLoaded = await cardStore.getCardsRequest()
    if (!cardsLoaded) throw new Error('Could not load the Differentiation cards.')

    router.push('/quiz')
  } catch (err) {
    error.value = err.message || 'Could not start the sample quiz.'
    starting.value = false
  }
}
</script>

<template>
  <Navbar />
  <main class="guide">
    <header class="hero">
      <p class="eyebrow">How the quiz was built</p>
      <h1 class="title">A quiz generator without a language model</h1>
      <p class="intro">
        This was a 2022 hobby, before I reached for a large language model. I wanted a quiz that came from my own flashcards,
        so I tried the pieces by hand. RAKE pulled keywords out of an answer. Word sense disambiguation picked which meaning of a word fitted the course.
        Co-hyponyms from WordNet became the wrong answers in a multiple choice question, words that sit beside the right one under the same category.
        I also looked at word vectors with word2vec, to see if nearby vectors made better distractors than the thesaurus approach.
        Separately, I trained decision trees in scikit-learn on revision history, to guess how many days should pass before a chapter came due again.
        None of that is a finished product. It is the trail of ideas that the quiz still runs on.
      </p>
    </header>

    <div class="layout">
      <section class="card">
        <h2><span>1</span> From a card to a question</h2>
        <ol>
          <li><strong>Your answer is the source.</strong> The generator reads the answer on the card, not a model prompt.</li>
          <li><strong>RAKE finds the phrases.</strong> It ranks keywords and drops digits and symbols.</li>
          <li><strong>Some phrases are blanked</strong> in the order they appear in the sentence.</li>
          <li><strong>WordNet writes the wrong answers.</strong> The course name, such as Maths, keeps those words in the same subject.</li>
          <li><strong>The real phrase is mixed in</strong> at a random position, so there are four choices.</li>
          <li><strong>If that fails, it changes type.</strong> No related words means fill-in-the-blank or reveal. No keywords at all means reveal.</li>
        </ol>
      </section>

      <section class="card">
        <h2><span>2</span> After you finish</h2>
        <p>
          Mistakes are compared with how many answers you gave. That score, the days since the last revision, and the course
          go into a scikit-learn decision tree. The tree returns a number of days until the chapter is due.
        </p>
        <p>
          It starts from a small default dataset. A drop-off, forgetting after a gap, retrains the tree on your past drop-offs
          plus that default data. Course ids are one-hot encoded so subjects stay separate. This was a scheduling experiment, not a finished memory model.
        </p>
      </section>
    </div>

    <section class="start">
      <div>
        <h2>Try it on Differentiation</h2>
        <p>Runs the real generator on the Differentiation chapter in Maths.</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
      <button class="btn btn-primary" :disabled="starting" @click="startSampleQuiz">
        {{ starting ? 'Loading cards…' : 'Start quiz' }}
      </button>
    </section>
  </main>
</template>

<style scoped>
.guide {
  min-height: 100vh;
  padding: 6rem 1.5rem 3rem;
  background:
    radial-gradient(circle at top right, rgba(53, 172, 218, 0.18), transparent 28rem),
    #f6f8fc;
  color: #243044;
}

.hero,
.layout,
.start {
  max-width: 960px;
  margin: 0 auto;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.75rem;
  position: relative;
}

.eyebrow {
  margin: 0 0 0.4rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.78rem;
  color: #1d6d84;
}

.title {
  display: block;
  position: static;
  margin: 0;
  font-size: 2.35rem;
  font-weight: 650;
  line-height: 1.25;
  letter-spacing: -0.02em;
  color: #17324d;
}

.intro,
.card p,
.start p {
  margin: 0;
  max-width: 42rem;
  line-height: 1.65;
  color: #3d4d63;
}

.layout {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 1rem;
}

.card,
.start {
  background: white;
  border-radius: 24px;
  box-shadow: rgba(47, 145, 255, 0.08) 0 4px 14px;
}

.card {
  padding: 1.3rem 1.4rem 1.5rem;
}

h2 {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0 0 0.9rem;
  font-size: 1.2rem;
}

h2 span {
  width: 1.7rem;
  height: 1.7rem;
  border-radius: 8px;
  display: grid;
  place-items: center;
  background: #2a9bb5;
  color: white;
  font-size: 0.9rem;
}

ol {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

li {
  padding-left: 0.8rem;
  border-left: 3px solid #d5eef4;
  line-height: 1.45;
}

.card p + p {
  margin-top: 0.8rem;
}

.start {
  margin-top: 1rem;
  padding: 1.2rem 1.4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: linear-gradient(120deg, #ffffff, #f3fbfe);
}

.error {
  margin-top: 0.4rem;
  color: #c45555;
}

@media (max-width: 800px) {
  .layout,
  .start {
    grid-template-columns: 1fr;
    display: grid;
  }

  .title {
    font-size: 2.1rem;
  }
}
</style>
