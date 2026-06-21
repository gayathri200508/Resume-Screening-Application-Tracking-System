# 🧾 Resume Screening & Application Tracking System

An NLP-based mini project that automatically screens resumes (PDF/DOCX)
against a job description, extracts skills, ranks candidates by
relevance, and tracks each candidate's status through a simple
Application Tracking System (ATS) — all through an interactive
Streamlit web app.

> Built as a CRT Mini Project | Tech Stack: Python, spaCy, scikit-learn, Streamlit

---

## ✨ Features

- 📄 **Resume Parsing** — extracts raw text from `.pdf` and `.docx` resumes.
- 🧠 **NLP Skill Extraction** — uses spaCy's `PhraseMatcher` to detect 100+
  technical & soft skills (Python, SQL, Machine Learning, Communication, etc.).
- 📊 **Smart Matching & Ranking** — combines **TF-IDF cosine similarity**
  (overall contextual match) with a **skill-overlap score** (% of JD
  skills found in the resume) into one blended ranking score.
- ✅ **Application Tracking System** — saves screened candidates to a
  local SQLite database and lets you update their hiring status
  (`Applied → Shortlisted → Interview Scheduled → Hired/Rejected`).
- 🖥️ **Streamlit UI** — drag-and-drop resumes, paste/upload a job
  description, and view ranked results instantly. A CLI mode is also
  included for quick terminal testing.
- 🎯 **No heavy model downloads** — uses a lightweight spaCy blank
  pipeline + rule-based matcher, so it runs out-of-the-box on any
  machine (even with restricted internet/college lab PCs).

---

## 📁 Folder Structure

```
resume-screening-system/
├── app.py                          # Streamlit web app (main entry point)
├── cli.py                          # Optional terminal/CLI version
├── generate_sample_resumes.py      # Generates sample resumes for testing
├── requirements.txt
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── resume_parser.py            # PDF/DOCX text extraction
│   ├── skill_extractor.py          # spaCy-based skill/entity extraction
│   ├── skills_db.py                # Master list of known skills
│   ├── matcher.py                  # TF-IDF similarity + ranking logic
│   └── tracker.py                  # SQLite Application Tracking System
├── data/
│   ├── sample_job_description.txt
│   └── sample_resumes/             # 3 ready-made sample resumes
└── docs/
    └── Project_Report.pdf          # 2-3 page project report
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/resume-screening-system.git
cd resume-screening-system
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> No `spacy download` step needed — the project uses a lightweight
> blank spaCy pipeline, so all skill matching works immediately after
> `pip install`.

### 4. (Optional) Generate sample resumes for testing
Three demo resumes (2 DOCX + 1 PDF) are already included in
`data/sample_resumes/`. To regenerate them at any time:
```bash
python generate_sample_resumes.py
```

---

## ▶️ How to Run

### Option A — Streamlit Web App (recommended for demo)
```bash
streamlit run app.py
```
This opens a browser window where you can:
1. Paste or upload a job description.
2. Upload one or more resumes (PDF/DOCX).
3. Click **"Screen & Rank Candidates"** to see ranked results with
   matched/missing skills.
4. Click **"Save to Application Tracker"** and switch to the
   **Application Tracker** tab to update each candidate's status.

### Option B — Command Line (quick test, no browser)
```bash
python cli.py --jd data/sample_job_description.txt --resumes data/sample_resumes/
```

---

## 🧮 How the Ranking Score Works

| Signal | What it measures | Weight |
|---|---|---|
| **Similarity Score** | TF-IDF cosine similarity between full resume text and JD text — captures overall contextual relevance | 50% |
| **Skill Match Score** | % of skills required in the JD that are actually present in the resume | 50% |

```
final_score = (0.5 × similarity_score) + (0.5 × skill_match_score)
```

Candidates are sorted in descending order of `final_score` to produce
the final ranked shortlist. Weights are configurable in `src/matcher.py`.

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **NLP:** spaCy (`PhraseMatcher`), regex (for email/phone extraction)
- **ML/Matching:** scikit-learn (`TfidfVectorizer`, cosine similarity)
- **File Parsing:** `pypdf` (PDF), `python-docx` (DOCX)
- **Database:** SQLite (built into Python — no setup needed)
- **UI:** Streamlit
- **Report generation:** ReportLab (used for `docs/Project_Report.pdf`)

---

## 🚀 Future Scope

- Use a transformer-based embedding model (e.g. Sentence-BERT) for
  deeper semantic matching instead of TF-IDF.
- Auto-extract years of experience and education level for finer
  filtering.
- Email/SMS notifications to candidates when their status changes.
- Multi-job-description support with a recruiter dashboard.
- Deploy on Streamlit Community Cloud / Render for a live public demo.

---

## 📄 License

This project was created for academic/educational purposes (CRT Mini
Project submission). Free to use and modify.
