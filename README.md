# Study App

A small hobby project for spaced-repetition flashcards. The interesting part is the quiz: it turns your own card answers into multiple choice, fill-in-the-blank, and reveal questions using keyword extraction (RAKE) and WordNet. No large language model is involved.

The interface is a Vue app. The API is Django with SQLite. Google sign-in is left on the login page marked **(DEPRECATED)**. The working path is **Continue with sample data**, which signs you into the bundled sample account while `DEBUG` is on.

## Sample data

Courses, chapters, and cards from the original local database are in `backend_django/fixtures/default_demo.json` (Maths / Differentiation is the chapter with cards). Load them after migrations:

```powershell
cd backend_django
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py loaddata fixtures/default_demo.json
..\.venv\Scripts\python.exe manage.py runserver
```

Frontend:

```powershell
cd frontend_vue
npm install
npm run dev
```

Open http://localhost:5173/login and use **Continue with sample data**.

## What is rough on purpose

- Layout and copy are unfinished.
- Only one chapter in the sample set has flashcards.
- Interval prediction is a small scikit-learn tree trained on revision history, not a production model.
- NLTK data (`punkt_tab`, stopwords, a local WordNet build) is downloaded on first quiz use.

## Security notes

Reviewed while preparing this copy:

- The Google OAuth client secret used to be hardcoded in settings and views, and an older `.env` was committed. Those values are removed from the tree. **Rotate that Google client secret** in Google Cloud; it remains in git history.
- Google login now reads `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` from the environment and is labeled deprecated in the UI.
- `DEBUG` is still on. The sample-account button calls `POST /auth/dev-login`, which only works when `DEBUG` is true.
- Flashcard and quiz-result endpoints now require the chapter to belong to the signed-in user.
- `SECRET_KEY` is still the Django starter key. Fine for a local demo, not for a public server.
