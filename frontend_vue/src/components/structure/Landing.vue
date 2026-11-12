<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="landing">
    <p class="eyebrow">A hobby project, left unfinished</p>
    <h1>Study Scope</h1>
    <p class="lead">
      Flashcards with a quiz generator I built to learn machine learning and natural language processing.
      Questions come from the cards themselves, using keyword extraction and WordNet, not a large language model.
    </p>
    <RouterLink to="/login" class="btn btn-primary">Log in</RouterLink>
    <ul>
      <li>Write a card, then turn the answer into multiple choice, fill-in-the-blank, or a reveal question.</li>
      <li>A small decision tree suggests when to revise a chapter again. It was an experiment, not a finished model.</li>
      <li>The interface and a lot of the data are still rough. This copy is here to show the idea.</li>
    </ul>
  </section>
</template>

<style scoped>
.landing {
  max-width: 40rem;
  margin: 0 auto;
  padding: 4.5rem 1.5rem 5rem;
  color: #243044;
}

.eyebrow {
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #5b6b82;
}

h1 {
  margin: 0;
  font-size: 3rem;
  font-weight: 650;
  letter-spacing: -0.03em;
  color: #17324d;
}

.lead {
  margin: 1.25rem 0 1.75rem;
  font-size: 1.15rem;
  line-height: 1.65;
}

ul {
  margin: 2.5rem 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

li {
  padding-left: 0.9rem;
  border-left: 3px solid #7ec8d4;
  line-height: 1.5;
  color: #3d4d63;
}
</style>
