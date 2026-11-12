# Study Scope

A 2022 hobby project for spaced-repetition flashcards. The quiz is generated from your own card answers with classical natural language processing, not a large language model. A small scikit-learn decision tree then suggests how many days should pass before that chapter is due again.

This repository is safe to show and to run on your own machine. It is not a public web service. Do not put the Django process on the internet.

## What you can walk through

1. Open the landing page. It explains what Study Scope was.
2. Sign in with **Continue with sample data**. Google sign-in is still on the page and marked deprecated. It does nothing unless you add your own OAuth credentials.
3. The dashboard is the old prototype layout. Its widgets are example data and say so.
4. **How the quiz works** describes the ideas that were tried: RAKE keyword extraction, word sense disambiguation, WordNet co-hyponyms as multiple-choice distractors, word2vec as another distractor idea, and decision trees in scikit-learn.
5. **Start quiz** runs the real generator on the Differentiation chapter in Maths.

## Run it locally

Backend, from the repository root:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend_django\requirements.txt
cd backend_django
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py loaddata fixtures/default_demo.json
..\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Frontend, in another terminal:

```powershell
cd frontend_vue
npm install
npm run dev
```

Open http://localhost:5173/login.

The first quiz can take a while. NLTK downloads `punkt_tab` and stopwords, and the quiz code loads a local WordNet build.

## Sample data

The database is SQLite. The sample account and cards are in `backend_django/fixtures/default_demo.json`. **Continue with sample data** only works while the backend is running locally.
