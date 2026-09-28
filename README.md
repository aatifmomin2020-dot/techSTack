# Developer Portfolio Tech Stack Predictor

A production-quality **AI/ML-Powered Developer Career & Portfolio Advisor**. 

Given a developer's GitHub profile, current skills, experience level, and target career role, this application analyzes their portfolio, calculates a 5-factor strength score (0–100), identifies skill gaps using deterministic comparison, predicts optimal technology stacks using **TF-IDF Feature Engineering and Cosine Similarity**, matches missing skills to curated portfolio projects, generates a personalized learning roadmap, and enriches career feedback with server-side Gemini AI insights.

---

## 🌟 Architecture & Core Product Flow

```
Developer
   │
   ├──> GitHub Username ────> GitHub REST API ────┐
   │                                              │
   └──> Manual Skill Input ───────────────────────┼──> Data Collection & Skill Extraction
                                                  │
┌─────────────────────────────────────────────────┴────────────────────────────────────────┐
│ Skill Extraction & Alias Normalization (JS → JavaScript, Py → Python, Postgres → PostgreSQL)│
└─────────────────────────────────────────────────┬────────────────────────────────────────┘
                                                  │
┌─────────────────────────────────────────────────┴────────────────────────────────────────┐
│ Portfolio Analysis & Strength Score (Diversity 25%, Complexity 25%, Activity 20%, Doc 15%, Rel 15%) │
└─────────────────────────────────────────────────┬────────────────────────────────────────┘
                                                  │
         ┌────────────────────────────────────────┴─────────────────────────────────┐
         │                                                                          │
         ▼                                                                          ▼
┌─────────────────────────────┐                                    ┌─────────────────────────────┐
│ Deterministic Skill Gap     │                                    │  ML Tech Stack Predictor    │
│ Set Comparison Logic        │                                    │  (TF-IDF + Cosine Sim)     │
└────────┬────────────────────┘                                    └────────┬────────────────────┘
         │                                                                  │
         ▼                                                                  ▼
┌─────────────────────────────┐                                    ┌─────────────────────────────┐
│ Project Gap Matcher Engine  │                                    │  Personalized Roadmap       │
│ (30+ Curated Projects)      │                                    │  (Topological Dependency)   │
└────────┬────────────────────┘                                    └────────┬────────────────────┘
         │                                                                  │
         └────────────────────────────────────────┬─────────────────────────┘
                                                  │
                                                  ▼
                               ┌────────────────────────────────────────┐
                               │  Gemini AI Qualitative Feedback Engine  │
                               └──────────────────┬─────────────────────┘
                                                  │
                                                  ▼
                               ┌────────────────────────────────────────┐
                               │ React 18 Dark Dashboard (Recharts UI)  │
                               └────────────────────────────────────────┘
```

---

## ⚙️ Methodology & Component Breakdown

| Feature / Subsystem | Implementation Type | Description & Mathematical Formula |
| :--- | :--- | :--- |
| **Skill Gap Detection** | **Deterministic Backend** | Exact mathematical set difference between target role required technologies and developer existing skills: \(\text{Missing} = R_{\text{required}} \setminus S_{\text{user}}\). |
| **Portfolio Strength Score** | **Empirical Mathematical Model** | 5 weighted components (Skill Diversity 25%, Project Complexity 25%, GitHub Activity 20%, Documentation Quality 15%, Technology Relevance 15%). Score constrained to \(0 \le \text{Score} \le 100\). |
| **Tech Stack Recommendation** | **Machine Learning (TF-IDF + Cosine Similarity)** | Vectorizes skill profiles into TF-IDF space and computes Cosine Similarity: <br> $$\text{similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$ |
| **Project Recommendation** | **Algorithmic Graph Matcher** | Ranks 30+ curated real-world projects based on missing skill coverage and difficulty. |
| **Personalized Learning Roadmap** | **Topological Dependency Engine** | Orders missing skills using prerequisite DAG graphs (e.g. JavaScript \(\rightarrow\) TypeScript \(\rightarrow\) React; Python \(\rightarrow\) Pandas \(\rightarrow\) PyTorch). |
| **Qualitative Feedback** | **Generative AI (Gemini 2.5)** | Server-side Gemini API calls for executive summary, career advice, and README optimization tips. |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js v18+ & npm
- SQLite (built-in) or PostgreSQL

---

### 1. Backend Setup

```bash
cd backend

# Install python dependencies
pip install -r requirements.txt

# Initialize & seed SQLite / PostgreSQL database
python -m app.db.init_db

# Train ML TF-IDF Vectorizer & export artifacts
python -m app.ml.model_training

# Run Pytest backend test suite (7 tests)
pytest

# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Backend API will be running at `http://localhost:8000` with interactive Swagger docs at `http://localhost:8000/docs`.

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run production build check
npm run build

# Start Vite dev server
npm run dev
```
Frontend will be running at `http://localhost:5173`.

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` in the backend directory:

```env
DATABASE_URL=sqlite:///./tech_stack_predictor.db
GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET=super-secret-key-2026
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check endpoint returning status and DB connection. |
| `GET` | `/api/skills` | Centralized skills catalog with categories and aliases. |
| `GET` | `/api/roles` | List of 10+ industry developer career roles. |
| `GET` | `/api/github/{username}` | Real GitHub API integration fetching user repos and topics. |
| `POST` | `/api/analysis` | Complete end-to-end portfolio analysis execution. |
| `GET` | `/api/analysis/{id}` | Retrieve historical analysis by ID. |
| `POST` | `/api/recommendations` | ML TF-IDF technology stack recommendations. |
| `GET` | `/api/projects/recommended` | Curated project recommendations matching skill gaps. |
| `POST` | `/api/roadmap` | Multi-phase learning roadmap generator. |
| `POST` | `/api/auth/register` | JWT user registration. |
| `POST` | `/api/auth/login` | JWT user login. |

---

## 🧪 Testing Summary

- **Backend Pytest Test Suite**: 7 unit & API integration tests passing cleanly.
- **Frontend Production Build**: Vite production build compiled with 0 errors (`npm run build`).

---

## 🌐 Deployment Instructions

- **Frontend**: Deploy `frontend/` to **Vercel** or **Netlify** using Vite build command `npm run build` and output directory `dist`. `vercel.json` rewrite configuration is provided.
- **Backend**: Deploy `backend/` to **Render** using `render.yaml`. Build command: `pip install -r backend/requirements.txt && python -m app.db.init_db`.
- **Database**: PostgreSQL on **Neon**, **Supabase**, or **Render PostgreSQL** by updating `DATABASE_URL`.
