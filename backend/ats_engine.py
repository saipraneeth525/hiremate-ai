import re

# -----------------------------
# Extract skills from JD
# -----------------------------
def extract_jd_skills(jd_text):
    skill_library = [
        "Python", "Java", "C++", "C", "JavaScript",
        "React", "Node.js", "FastAPI", "Flask",
        "Django", "SQL", "MySQL", "PostgreSQL",
        "MongoDB", "Docker", "Kubernetes",
        "AWS", "Azure", "Git", "GitHub",
        "Machine Learning",
        "TensorFlow",
        "PyTorch"
    ]

    found = []

    jd_lower = jd_text.lower()

    for skill in skill_library:
        if skill.lower() in jd_lower:
            found.append(skill)

    return found


# -----------------------------
# Education Score
# -----------------------------
def education_score(education):
    if not education:
        return 0

    text = " ".join(education).lower()

    score = 0

    if "b.tech" in text or "btech" in text:
        score += 10

    if "computer" in text:
        score += 5

    if "engineering" in text:
        score += 5

    return min(score, 20)


# -----------------------------
# Experience Score
# -----------------------------
def experience_score(experience):

    if not experience:
        return 0

    years = 0

    text = " ".join(experience)

    matches = re.findall(r"\d+", text)

    if matches:
        years = max(int(x) for x in matches)

    return min(years * 5, 20)


# -----------------------------
# Projects Score
# -----------------------------
def project_score(projects):

    if not projects:
        return 0

    return min(len(projects) * 3, 15)


# -----------------------------
# Certification Score
# -----------------------------
def certification_score(certifications):

    if not certifications:
        return 0

    return min(len(certifications) * 2, 10)


# -----------------------------
# Main ATS
# -----------------------------
def calculate_resume_score(jd_text, candidate_skills,
                           education=None,
                           experience=None,
                           projects=None,
                           certifications=None):

    jd_skills = extract_jd_skills(jd_text)

    matched = []

    missing = []

    for skill in jd_skills:
        if skill.lower() in [s.lower() for s in candidate_skills]:
            matched.append(skill)
        else:
            missing.append(skill)

    if jd_skills:
        skill_score = (len(matched) / len(jd_skills)) * 35
    else:
        skill_score = 35

    edu_score = education_score(education)

    exp_score = experience_score(experience)

    proj_score = project_score(projects)

    cert_score = certification_score(certifications)

    total = round(
        skill_score +
        edu_score +
        exp_score +
        proj_score +
        cert_score
    )

    total = min(total, 100)

    return {
        "ats_score": total,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_score": round(skill_score),
        "education_score": edu_score,
        "experience_score": exp_score,
        "project_score": proj_score,
        "certification_score": cert_score
    }