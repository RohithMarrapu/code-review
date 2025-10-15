# Code Review Assistant (Transformers + FastAPI + Streamlit)

A minimal full-stack app that accepts source code and produces an AI-generated review using HuggingFace Transformers (FLAN-T5). Includes an optional dashboard to upload files and view past reports. Uses SQLite for storage.

## Features
- FastAPI backend with endpoints to upload code and fetch stored reviews
- Transformers-based reviewer using `google/flan-t5-base` (CPU-friendly)
- SQLite persistence via SQLAlchemy
- Streamlit dashboard to upload code and browse reports

## Architecture
- `backend/` FastAPI app, SQLAlchemy models, and Transformers integration
- `frontend/` Streamlit single-page app

## Getting Started

### 1) Create a virtual environment
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run the backend
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
Open API docs at `http://127.0.0.1:8000/docs`.

### 4) Run the dashboard
```bash
streamlit run frontend/app.py
```
Set API base URL in the left sidebar if different (defaults to `http://127.0.0.1:8000`).

## API
- `POST /api/review` multipart/form-data
  - fields: `file` (optional), `content` (optional), `filename` (optional), `language` (optional)
  - returns: stored review record
- `GET /api/reviews`
  - returns: list of recent reviews
- `GET /api/reviews/{id}`
  - returns: single review

## LLM Prompt
The backend constructs a structured prompt:
> Review this code for readability, modularity, maintainability, and potential bugs. Return a structured review with sections: Overview, Strengths, Issues (with severity), and Actionable Suggestions.

You can swap the model in `backend/llm.py` if you prefer a different HF pipeline.

## Notes
- First run will download the model (`flan-t5-base`).
- For better results or faster inference, replace the model with a local or quantized variant.
- SQLite DB file is `reviews.db` in project root.

## Demo Video
- Record a short screencast: start backend, run Streamlit, upload a file, show the review and history.

## License
MIT


