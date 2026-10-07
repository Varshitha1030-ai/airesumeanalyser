# AI Resume Analyzer

A Streamlit app that analyses a resume (PDF or DOCX) and compares it with a job description.

**Features**
- Extracts text from PDF and DOCX resumes
- Detects 150+ technical and soft skills
- ATS-style score (0-100) with a breakdown
- Matched vs missing skills for a given job description
- Resume-to-job similarity (TF-IDF, or an optional semantic model)

## Run locally
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this repo to GitHub.
2. Go to https://share.streamlit.io and click **Create app**.
3. Pick your repo, branch `main`, and main file path `app.py`.
4. Under **Advanced settings**, choose Python 3.11 or 3.12, then **Deploy**.

## Optional: semantic AI similarity
Add these two lines to `requirements.txt` to enable the sentence-transformers model
(the first run downloads ~90 MB and the build is much slower):
```
sentence-transformers
torch
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit interface |
| `resume_parser.py` | PDF / DOCX text extraction |
| `skills.py` | Skill list and skill detection |
| `ats.py` | ATS score |
| `compare.py` | Matching and missing skills |
| `similarity.py` | Resume vs job similarity |
