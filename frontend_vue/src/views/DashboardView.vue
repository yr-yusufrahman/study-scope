<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import Navbar from '@/components/structure/Navbar.vue'
import schoolIcon from '@/components/icons/dashboard/school.svg?raw'
import psychologyIcon from '@/components/icons/dashboard/psychology.svg?raw'
import listIcon from '@/components/icons/dashboard/list.svg?raw'
import examIcon from '@/components/icons/dashboard/exam.svg?raw'
import calendarIcon from '@/components/icons/dashboard/calendar_month.svg?raw'

const exampleNote = 'Example, not your data'

const plan = [
  { course: 'Maths', name: 'Differentiation', done: false },
  { course: 'Maths', name: 'Integration', done: true },
  { course: 'Physics', name: 'Waves', done: false },
]
const planCourses = [...new Set(plan.map((item) => item.course))]
const planProgress = Math.round((plan.filter((item) => item.done).length / plan.length) * 100)

const memories = [
  {
    name: 'Differentiation',
    rating: 'High',
    tone: '#31CF8E',
    last: '2 days ago',
    started: '12/03/2024',
    points: [0, 1, 1, 2, 2],
  },
  {
    name: 'Market failure',
    rating: 'Medium',
    tone: '#ffbd59',
    last: '6 days ago',
    started: '02/02/2024',
    points: [2, 1, 0, 1],
  },
  {
    name: 'Waves',
    rating: 'Low',
    tone: '#FF5757',
    last: 'Today',
    started: '20/01/2024',
    points: [1, 0, 0, 1],
  },
]
const memoryIndex = ref(0)
const memory = computed(() => memories[memoryIndex.value])

const memoryPath = computed(() => {
  const values = memory.value.points
  return values
    .map((value, index) => {
      const x = 16 + (index * 220) / Math.max(values.length - 1, 1)
      const y = 96 - value * 32
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`
    })
    .join(' ')
})

const todos = [
  { name: 'Organise books', done: true },
  { name: 'Finish maths homework', done: false },
]

const exams = [
  { name: 'Maths paper', left: '18 days', value: 72 },
  { name: 'Physics practical', left: '41 days', value: 34 },
  { name: 'Economics essay', left: '55 days', value: 12 },
]

function examColor(value) {
  if (value > 70) return '#FF5757'
  if (value > 30) return '#FFAD57'
  return '#FFDE59'
}

const today = new Date()
const monthLabel = today.toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
const selectedDay = ref(today.getDate())
const weekdayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const calendarDays = computed(() => {
  const year = today.getFullYear()
  const month = today.getMonth()
  const first = new Date(year, month, 1)
  const startOffset = (first.getDay() + 6) % 7
  const count = new Date(year, month + 1, 0).getDate()
  const cells = Array.from({ length: startOffset }, () => null)
  for (let day = 1; day <= count; day += 1) cells.push(day)
  return cells
})

const sampleMarks = {
  4: 'revision',
  9: 'exam',
  11: 'both',
  18: 'revision',
  22: 'exam',
}

const dayDetail = computed(() => {
  const kind = sampleMarks[selectedDay.value]
  if (kind === 'exam' || kind === 'both') {
    return { title: 'Exams', lines: ['Maths paper · Maths'] }
  }
  if (kind === 'revision') {
    return { title: 'Revision', lines: ['Differentiation · Maths'] }
  }
  return { title: 'Nothing scheduled', lines: [] }
})
</script>

<template>
  <Navbar />
  <main class="dashboard">
    <div class="banner-row">
      <p class="banner">{{ exampleNote }}. These panels are the prototype dashboard, filled in so the layout is recognisable.</p>
      <RouterLink to="/quiz-guide" class="btn btn-primary">How the quiz works</RouterLink>
    </div>

    <div class="top">
      <section>
        <div class="heading">
          <h2>Today's plan</h2>
          <span class="swatch" style="background: #64beff" v-html="schoolIcon"></span>
        </div>
        <div class="card plan">
          <div class="ring" :style="{ '--progress': planProgress }">
            <strong>{{ planProgress }}%</strong>
          </div>
          <div v-for="course in planCourses" :key="course" class="course-block">
            <span class="pill">{{ course }}</span>
            <div v-for="item in plan.filter((entry) => entry.course === course)" :key="item.name" class="line">
              <span>{{ item.name }}</span>
              <span class="tick" :class="{ done: item.done }"></span>
            </div>
          </div>
        </div>
      </section>

      <section class="memory-column">
        <div class="heading">
          <h2>Memory</h2>
          <span class="swatch" style="background: #ff5881" v-html="psychologyIcon"></span>
        </div>
        <div class="card memory">
          <div class="memory-title">
            <h3>{{ memory.name }}</h3>
            <span class="rating" :style="{ color: memory.tone, background: memory.tone + '22' }">{{ memory.rating }}</span>
          </div>
          <div class="memory-body">
            <div class="side">
              <span>Last</span>
              <small>{{ memory.last }}</small>
            </div>
            <svg viewBox="0 0 250 110" class="graph" aria-hidden="true">
              <path :d="memoryPath" fill="none" :stroke="memory.tone" stroke-width="3" stroke-linecap="round" />
              <text x="4" y="20" class="axis">Easy</text>
              <text x="4" y="52" class="axis">Okay</text>
              <text x="4" y="84" class="axis">Hard</text>
            </svg>
            <div class="side">
              <span>Started</span>
              <small>{{ memory.started }}</small>
            </div>
          </div>
          <div class="dots">
            <button
              v-for="(item, index) in memories"
              :key="item.name"
              :class="{ active: index === memoryIndex }"
              :aria-label="item.name"
              @click="memoryIndex = index"
            ></button>
          </div>
        </div>

        <div class="split">
          <section>
            <div class="heading">
              <h2>To-do list</h2>
              <span class="swatch" style="background: #76db74" v-html="listIcon"></span>
            </div>
            <div class="card">
              <div v-for="item in todos" :key="item.name" class="line">
                <span>{{ item.name }}</span>
                <span class="tick" :class="{ done: item.done }"></span>
              </div>
            </div>
          </section>
          <section>
            <div class="heading">
              <h2>Exams</h2>
              <span class="swatch" style="background: #ffde59" v-html="examIcon"></span>
            </div>
            <div class="card">
              <div v-for="exam in exams" :key="exam.name" class="exam">
                <span>{{ exam.name }}</span>
                <span class="bar"><span :style="{ width: exam.value + '%', background: examColor(exam.value) }"></span></span>
                <em>{{ exam.left }}</em>
              </div>
            </div>
          </section>
        </div>
      </section>
    </div>

    <section class="calendar-section">
      <div class="heading">
        <h2>Calendar</h2>
        <span class="swatch" style="background: #8080ff" v-html="calendarIcon"></span>
      </div>
      <div class="card calendar">
        <div>
          <div class="legend">
            <span><i class="dot revise"></i> Revision</span>
            <span><i class="dot exam-dot"></i> Exam</span>
            <span><i class="dot both"></i> Both</span>
          </div>
          <p class="month">{{ monthLabel }}</p>
          <div class="weekdays">
            <span v-for="label in weekdayLabels" :key="label">{{ label }}</span>
          </div>
          <div class="days">
            <button
              v-for="(day, index) in calendarDays"
              :key="index"
              :disabled="!day"
              :class="{ selected: day === selectedDay, [sampleMarks[day] || '']: Boolean(day) }"
              @click="day && (selectedDay = day)"
            >
              {{ day || '' }}
            </button>
          </div>
        </div>
        <aside>
          <h3>{{ selectedDay }} {{ monthLabel }}</h3>
          <p>{{ dayDetail.title }}</p>
          <p v-for="line in dayDetail.lines" :key="line">{{ line }}</p>
        </aside>
      </div>
    </section>
  </main>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 5.5rem 1.25rem 2.5rem;
  background: #f7f8fb;
  color: #243044;
}

.banner,
.month,
aside p {
  color: #6b7288;
}

.banner-row {
  max-width: 1100px;
  margin: 0 auto 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.banner {
  margin: 0;
}

.top,
.calendar-section {
  max-width: 1100px;
  margin: 0 auto;
}

.top {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  gap: 1.5rem;
}

.memory-column,
.split {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.7rem;
}

h2 {
  margin: 0;
  font-size: 1.7rem;
  font-weight: 600;
}

.swatch {
  width: 2rem;
  height: 2rem;
  border-radius: 6px;
  display: grid;
  place-items: center;
  color: white;
}

.swatch :deep(svg) {
  width: 1.25rem;
  height: 1.25rem;
}

.swatch :deep(path),
.swatch :deep(circle) {
  fill: currentColor;
}

.swatch :deep([fill='none']) {
  fill: none;
}

.card {
  background: white;
  border-radius: 28px;
  padding: 1.1rem 1.2rem;
  box-shadow: rgba(47, 145, 255, 0.08) 0 4px 14px;
}

.plan,
.course-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.ring {
  width: 5.5rem;
  height: 5.5rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: conic-gradient(#64beff calc(var(--progress) * 1%), #f2faff 0);
}

.ring strong {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: white;
}

.pill {
  background: #80d0c7;
  color: white;
  border-radius: 6px;
  padding: 0.15rem 0.9rem;
}

.line,
.exam {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 0.6rem;
}

.exam {
  grid-template-columns: 1fr 1fr auto;
  margin-bottom: 0.8rem;
}

.tick {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background: #d0e1e7;
}

.tick.done {
  background: #31cf8e;
}

.memory-title,
.dots,
.legend,
.weekdays,
.days {
  display: flex;
  justify-content: center;
  align-items: center;
}

.memory-title {
  gap: 0.7rem;
}

.memory-title h3 {
  margin: 0;
  font-size: 1.15rem;
}

.rating {
  border-radius: 8px;
  padding: 0.1rem 0.7rem;
}

.memory-body {
  display: grid;
  grid-template-columns: 4.5rem 1fr 4.5rem;
  align-items: center;
  min-height: 8rem;
}

.side {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #bec3dd;
  text-align: center;
}

.graph {
  width: 100%;
  height: 7.5rem;
}

.axis {
  fill: #bec3dd;
  font-size: 11px;
}

.dots {
  gap: 0.35rem;
}

.dots button {
  width: 0.75rem;
  height: 0.75rem;
  border: 0;
  border-radius: 50%;
  background: #d0e1e7;
  cursor: pointer;
}

.dots button.active {
  background: #ff5881;
}

.bar {
  height: 0.45rem;
  background: #f2faff;
  border-radius: 99px;
  overflow: hidden;
}

.bar span {
  display: block;
  height: 100%;
}

.calendar {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr;
  gap: 1rem;
}

.legend {
  justify-content: flex-start;
  gap: 1rem;
  margin-bottom: 0.6rem;
}

.dot {
  display: inline-block;
  width: 0.7rem;
  height: 0.7rem;
  border-radius: 50%;
  margin-right: 0.3rem;
}

.revise { background: #31cf8e; }
.exam-dot { background: #8080ff; }
.both { background: #ff5757; }

.weekdays,
.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.25rem;
  text-align: center;
}

.days button {
  border: 0;
  background: transparent;
  border-radius: 10px;
  min-height: 2.2rem;
  cursor: pointer;
  color: inherit;
}

.days button.selected {
  outline: 2px solid #64beff;
}

.days button.revision { box-shadow: inset 0 -3px 0 #31cf8e; }
.days button.exam { box-shadow: inset 0 -3px 0 #8080ff; }
.days button.both { box-shadow: inset 0 -3px 0 #ff5757; }

aside h3 {
  margin: 0 0 0.4rem;
}

@media (max-width: 900px) {
  .top,
  .split,
  .calendar,
  .memory-body {
    grid-template-columns: 1fr;
  }
}
</style>
