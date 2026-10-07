"""A transparent, explainable ATS-style score (0-100)."""
import re

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{8,}\d)")

SECTIONS = {
    "Education": ["education", "academic"],
    "Experience": ["experience", "internship", "employment", "work history"],
    "Skills": ["skills", "technical skills", "core competencies"],
    "Projects": ["projects", "project work"],
}


def detect_sections(text: str) -> dict:
    low = text.lower()
    return {name: any(k in low for k in keys) for name, keys in SECTIONS.items()}


def ats_score(resume_text, resume_skills, job_skills=None):
    """Return (score, breakdown).

    Weights: keyword match 50 (or skill breadth 50 when no job description),
    sections 25, contact info 15, length 10.
    """
    breakdown = {}

    if job_skills:
        matched = {s.lower() for s in resume_skills} & {s.lower() for s in job_skills}
        keyword = len(matched) / len(job_skills) * 50
        breakdown["Keyword match with job"] = round(keyword, 1)
    else:
        keyword = min(len(resume_skills) / 12, 1) * 50  # 12+ recognised skills = full marks
        breakdown["Skill breadth"] = round(keyword, 1)

    sections = detect_sections(resume_text)
    section_pts = sum(sections.values()) / len(sections) * 25
    breakdown["Resume sections"] = round(section_pts, 1)

    contact = 0
    if EMAIL_RE.search(resume_text):
        contact += 8
    if PHONE_RE.search(resume_text):
        contact += 7
    breakdown["Contact info"] = contact

    words = len(resume_text.split())
    if 300 <= words <= 900:
        length_pts = 10
    elif 150 <= words < 300 or 900 < words <= 1300:
        length_pts = 6
    else:
        length_pts = 2
    breakdown["Length"] = length_pts

    total = round(min(keyword + section_pts + contact + length_pts, 100), 1)
    return total, breakdown


if __name__ == "__main__":
    print(ats_score("education skills projects a@b.com 9876543210", ["Python", "SQL"]))
