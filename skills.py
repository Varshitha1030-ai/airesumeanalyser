"""Skill database and skill extraction from free text."""
import re

# canonical skill -> extra spellings that should map to it
SKILLS = {
    # languages
    "Python": [], "Java": [], "JavaScript": ["js", "ecmascript"], "TypeScript": [],
    "C": [], "C++": [], "C#": [], "Go": ["golang"], "Rust": [], "Kotlin": [],
    "Swift": [], "PHP": [], "Ruby": [], "R": [], "MATLAB": [], "Scala": [],
    "Bash": ["shell scripting"], "SQL": [],
    # web
    "HTML": ["html5"], "CSS": ["css3"], "React": ["react.js", "reactjs"],
    "Angular": [], "Vue": ["vue.js", "vuejs"], "Node.js": ["nodejs"],
    "Express": ["express.js"], "Next.js": ["nextjs"], "Tailwind CSS": ["tailwind"],
    "Bootstrap": [], "REST API": ["restful", "rest apis", "restful api", "restful apis"],
    "GraphQL": [],
    # python frameworks
    "Flask": [], "Django": [], "FastAPI": [], "Streamlit": [],
    # data / ML
    "Machine Learning": ["ml"], "Deep Learning": [], "NLP": ["natural language processing"],
    "Computer Vision": [], "Data Analysis": ["data analytics"],
    "Data Science": [], "Statistics": [], "Pandas": [], "NumPy": [],
    "Scikit-learn": ["sklearn", "scikit learn"], "TensorFlow": [], "PyTorch": [],
    "Keras": [], "OpenCV": [], "spaCy": [], "NLTK": [], "Transformers": ["hugging face", "huggingface"],
    "LLM": ["llms", "large language models"], "Generative AI": ["genai", "gen ai"],
    "Matplotlib": [], "Seaborn": [], "Plotly": [], "Power BI": ["powerbi"],
    "Tableau": [], "Excel": ["ms excel", "microsoft excel"], "ETL": [],
    "Data Visualization": ["data visualisation"], "Feature Engineering": [],
    # databases
    "MySQL": [], "PostgreSQL": ["postgres"], "MongoDB": ["mongo"], "SQLite": [],
    "Redis": [], "Oracle": [], "Firebase": [], "NoSQL": [],
    # cloud / devops
    "AWS": ["amazon web services"], "Azure": [], "GCP": ["google cloud"],
    "Docker": [], "Kubernetes": ["k8s"], "Git": [], "GitHub": [], "GitLab": [],
    "CI/CD": ["ci cd", "cicd"], "Linux": [], "Jenkins": [], "Terraform": [],
    # general / CS
    "Data Structures": ["dsa"], "Algorithms": [], "OOP": ["object oriented programming", "object-oriented programming"],
    "System Design": [], "Microservices": [], "Agile": [], "Scrum": [],
    "Unit Testing": ["pytest", "unittest"], "Postman": [], "Jira": [],
    # soft skills
    "Communication": [], "Leadership": [], "Teamwork": ["team work"],
    "Problem Solving": ["problem-solving"], "Time Management": [],
    "Critical Thinking": [],
}

# alias (lowercase) -> canonical name
_LOOKUP = {}
for canonical, aliases in SKILLS.items():
    _LOOKUP[canonical.lower()] = canonical
    for alias in aliases:
        _LOOKUP[alias.lower()] = canonical

# Words that are also common English words: only match with this exact capitalisation.
_CASE_SENSITIVE = {
    "go": "Go", "ml": "ML", "swift": "Swift", "ruby": "Ruby",
    "express": "Express", "oracle": "Oracle", "excel": "Excel",
}
# One-letter skills match far too much prose; accept them only in list-like positions.
_SINGLE_LETTER = {"c": "C", "r": "R"}

# "." is excluded before a term so that the "js" in "Node.js" is not read as JavaScript.
_BEFORE = r"(?<![A-Za-z0-9+#.])"
_AFTER = r"(?![A-Za-z0-9+#])"
_LISTLIKE = r"(?=\s*[,|/;).]|\s+and\b|\s*$)"

_PATTERNS = []
for term in sorted(_LOOKUP, key=len, reverse=True):  # longest first
    if term in _SINGLE_LETTER:
        regex = re.compile(_BEFORE + _SINGLE_LETTER[term] + _AFTER + _LISTLIKE)
    elif term in _CASE_SENSITIVE:
        regex = re.compile(_BEFORE + re.escape(_CASE_SENSITIVE[term]) + _AFTER)
    else:
        regex = re.compile(_BEFORE + re.escape(term) + _AFTER, re.IGNORECASE)
    _PATTERNS.append((_LOOKUP[term], regex))


def extract_skills(text: str) -> list:
    """Return a sorted list of canonical skill names found in `text`."""
    if not text:
        return []
    found = {canonical for canonical, regex in _PATTERNS if regex.search(text)}
    return sorted(found, key=str.lower)
