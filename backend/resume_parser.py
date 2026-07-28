import re

SKILLS = [
    "Python", "Java", "C++", "C", "JavaScript",
    "React", "Node.js", "FastAPI", "Flask",
    "Django", "SQL", "MySQL", "PostgreSQL",
    "MongoDB", "Docker", "Kubernetes",
    "AWS", "Azure", "Git", "GitHub",
    "Machine Learning", "TensorFlow", "PyTorch"
]


def extract_section(text, section_names):
    """
    Extract lines under a heading until the next heading.
    """
    lines = text.splitlines()
    result = []
    capture = False

    headings = [
        "education",
        "experience",
        "projects",
        "certifications",
        "skills",
        "technical skills",
        "internships",
        "achievements",
        "summary",
        "objective"
    ]

    for line in lines:
        clean = line.strip()

        if not clean:
            continue

        lower = clean.lower()

        if lower in [s.lower() for s in section_names]:
            capture = True
            continue

        if capture:
            if lower in headings:
                break
            result.append(clean)

    return result


def parse_resume(text: str):
    """
    Parse resume into structured JSON.
    """

    # --------------------------
    # Email
    # --------------------------

    email = ""

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    if email_match:
        email = email_match.group()

    # --------------------------
    # Phone
    # --------------------------

    phone = ""

    phone_match = re.search(
        r"\+?\d[\d\s\-]{8,15}",
        text,
    )

    if phone_match:
        phone = phone_match.group().strip()

    # --------------------------
    # Name
    # --------------------------

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    candidate = lines[0] if lines else "Unknown"

    # --------------------------
    # Skills
    # --------------------------

    skills = []

    lower_text = text.lower()

    for skill in SKILLS:
        if skill.lower() in lower_text:
            skills.append(skill)

    # --------------------------
    # Education
    # --------------------------

    education = extract_section(
        text,
        ["Education", "Academic Background"]
    )

    # --------------------------
    # Experience
    # --------------------------

    experience = extract_section(
        text,
        ["Experience", "Work Experience", "Internships"]
    )

    # --------------------------
    # Projects
    # --------------------------

    projects = extract_section(
        text,
        ["Projects", "Project"]
    )

    # --------------------------
    # Certifications
    # --------------------------

    certifications = extract_section(
        text,
        ["Certifications", "Certificates"]
    )

    return {
        "candidate": candidate,
        "email": email,
        "phone": phone,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "skills": skills,
        "raw_text": text
    }