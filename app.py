"""AI Resume Analyzer - Streamlit app.  Run:  streamlit run app.py"""
import streamlit as st

from ats import ats_score, detect_sections
from compare import find_matching_skills, find_missing_skills
from resume_parser import extract_text
from similarity import semantic_available, similarity_percent
from skills import extract_skills

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.caption("Upload your resume, paste a job description, and see how well they match.")

with st.sidebar:
    st.header("Settings")
    if semantic_available():
        use_semantic = st.checkbox(
            "Use semantic AI model (slower, more accurate)", value=False,
            help="Uses sentence-transformers all-MiniLM-L6-v2.",
        )
    else:
        use_semantic = False
        st.info("Using fast TF-IDF matching. Install `sentence-transformers` to enable the semantic model.")
    st.markdown("---")
    st.markdown("Supported files: **PDF**, **DOCX**")

left, right = st.columns(2)
with left:
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx"])
with right:
    job_text = st.text_area("Paste job description (optional)", height=220,
                            placeholder="Paste the full job posting here...")

if st.button("Analyze", type="primary", disabled=uploaded is None):
    try:
        resume_text = extract_text(uploaded)
    except Exception as exc:  # corrupted / unsupported file
        st.error(f"Could not read this file: {exc}")
        st.stop()

    if len(resume_text.split()) < 30:
        st.warning(
            "Very little text was found. If your resume is a scanned image, "
            "export it as a text-based PDF or upload a DOCX instead."
        )
        st.stop()

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text) if job_text.strip() else []

    score, breakdown = ats_score(resume_text, resume_skills, job_skills or None)

    st.subheader("Results")
    c1, c2, c3 = st.columns(3)
    c1.metric("ATS score", f"{score}/100")
    c2.metric("Skills found", len(resume_skills))
    if job_text.strip():
        sim = similarity_percent(resume_text, job_text, use_semantic)
        c3.metric("Job similarity", f"{sim}%")
    else:
        c3.metric("Job similarity", "n/a")
    st.progress(min(int(score), 100) / 100)
    if job_text.strip() and not use_semantic:
        st.caption("TF-IDF similarity is strict: 15-40% already indicates a good match. "
                   "Use the skills tab and ATS score for the clearest picture.")

    tab_skills, tab_score, tab_text = st.tabs(["Skills", "Score breakdown", "Extracted text"])

    with tab_skills:
        st.markdown("**Skills found in resume**")
        st.write(", ".join(resume_skills) if resume_skills else "No known skills detected.")
        if job_skills:
            matched = find_matching_skills(resume_skills, job_skills)
            missing = find_missing_skills(resume_skills, job_skills)
            a, b = st.columns(2)
            with a:
                st.success(f"Matched ({len(matched)})")
                st.write(", ".join(matched) if matched else "None")
            with b:
                st.error(f"Missing ({len(missing)})")
                st.write(", ".join(missing) if missing else "Nothing missing - great match!")
        elif job_text.strip():
            st.info("No recognised skills were found in the job description.")

    with tab_score:
        for name, pts in breakdown.items():
            st.write(f"{name}: **{pts}** pts")
        sections = detect_sections(resume_text)
        absent = [n for n, ok in sections.items() if not ok]
        if absent:
            st.warning("Sections not detected: " + ", ".join(absent))

    with tab_text:
        st.text_area("Text read from your resume", resume_text, height=300)
