"""Compare resume skills against job skills."""


def find_missing_skills(resume_skills, job_skills):
    """Skills the job asks for that the resume does not list (case-insensitive)."""
    have = {s.lower() for s in resume_skills}
    return [s for s in job_skills if s.lower() not in have]


def find_matching_skills(resume_skills, job_skills):
    """Skills that appear in both lists (case-insensitive)."""
    have = {s.lower() for s in resume_skills}
    return [s for s in job_skills if s.lower() in have]


if __name__ == "__main__":
    print(find_missing_skills(["Python", "Flask", "SQL"],
                              ["Python", "Flask", "SQL", "React", "Machine Learning"]))
