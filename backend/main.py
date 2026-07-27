import os
import shutil
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

from file_utils import extract_text

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="HireMate AI",
    version="2.0"
)

# =====================================================
# Create Upload Directories
# =====================================================

os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/jd", exist_ok=True)
os.makedirs("uploads/resumes", exist_ok=True)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Request Models
# =====================================================

class AnalyzeRequest(BaseModel):
    question: str


class ChatRequest(BaseModel):
    message: str


# =====================================================
# Home
# =====================================================

@app.get("/")
def home():

    return {
        "message": "HireMate AI Backend Running 🚀"
    }


# =====================================================
# Upload Job Description
# =====================================================

@app.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):

    filepath = os.path.join(
        "uploads",
        "jd",
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "message": "Job Description uploaded successfully.",
        "filename": file.filename
    }


# =====================================================
# Upload Multiple Resumes
# =====================================================

@app.post("/upload-resumes")
async def upload_resumes(
    files: List[UploadFile] = File(...)
):

    uploaded_files = []

    for file in files:

        filepath = os.path.join(
            "uploads",
            "resumes",
            file.filename
        )

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    return {
        "success": True,
        "message": "Resumes uploaded successfully.",
        "total_files": len(uploaded_files),
        "files": uploaded_files
    }
    # =====================================================
# Helper Function - Load Job Description
# =====================================================

def load_job_description():

    jd_files = os.listdir("uploads/jd")

    if not jd_files:
        return None

    jd_path = os.path.join(
        "uploads",
        "jd",
        jd_files[0]
    )

    return extract_text(jd_path)


# =====================================================
# Helper Function - Load All Resumes
# =====================================================

def load_all_resumes():

    resume_files = os.listdir("uploads/resumes")

    if not resume_files:
        return None

    resumes = ""

    for filename in resume_files:

        filepath = os.path.join(
            "uploads",
            "resumes",
            filename
        )

        resume_text = extract_text(filepath)

        resumes += f"""

==================================================
Candidate Name: {filename}
==================================================

{resume_text}

"""

    return resumes


# =====================================================
# Test Job Description Extraction
# =====================================================

@app.get("/test-jd")
def test_jd():

    jd_files = os.listdir("uploads/jd")

    if not jd_files:

        return {
            "success": False,
            "message": "No Job Description uploaded."
        }

    jd_path = os.path.join(
        "uploads",
        "jd",
        jd_files[0]
    )

    text = extract_text(jd_path)

    return {
        "success": True,
        "filename": jd_files[0],
        "preview": text[:2000]
    }


# =====================================================
# Test Resume Extraction
# =====================================================

@app.get("/test-resumes")
def test_resumes():

    resume_files = os.listdir("uploads/resumes")

    if not resume_files:

        return {
            "success": False,
            "message": "No resumes uploaded."
        }

    data = []

    for filename in resume_files:

        filepath = os.path.join(
            "uploads",
            "resumes",
            filename
        )

        text = extract_text(filepath)

        data.append(
            {
                "filename": filename,
                "preview": text[:800]
            }
        )

    return {
        "success": True,
        "total_resumes": len(data),
        "resumes": data
    }
    # =====================================================
# Analyze Resumes (ATS + Recruiter Questions)
# =====================================================

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    # Load Job Description
    jd_text = load_job_description()

    if jd_text is None:
        return {
            "success": False,
            "error": "Please upload a Job Description first."
        }

    # Load Resumes
    resumes = load_all_resumes()

    if resumes is None:
        return {
            "success": False,
            "error": "Please upload resumes first."
        }

    prompt = f"""
You are HireMate AI.

You are an expert Technical Recruiter,
Senior HR Manager,
and Applicant Tracking System (ATS).

You must answer ONLY using the uploaded Job Description and Candidate Resumes.

==================================================
JOB DESCRIPTION
==================================================

{jd_text}

==================================================
CANDIDATE RESUMES
==================================================

{resumes}

==================================================
RECRUITER QUESTION
==================================================

{request.question}

==================================================
RULES
==================================================

If the recruiter asks for:

• Full ATS Report
• Analyze all resumes
• Rank candidates
• Best candidate
• Complete analysis

Generate a detailed ATS report.

For EACH candidate include:

# Candidate Name

## ATS Score (/100)

## Skills Matched

## Missing Skills

## Experience Match

## Education Match

## Relevant Projects

## Certifications

## Strengths

## Weaknesses

## Missing Keywords

## Hiring Decision

(Hire / Consider / Reject)

## Reason

## Interview Questions (5)

--------------------------------------------------

After all candidates provide:

# Final Ranking

Rank candidates from best to worst.

Explain why Rank 1 is best.

Finally generate:

# Dashboard Summary

- Total Candidates
- Best Candidate
- Highest ATS Score
- Candidates needing improvement
- Final Hiring Decision

--------------------------------------------------

If the recruiter asks any normal question such as:

Who has AWS certification?

Who has React experience?

Compare Candidate 1 and Candidate 2.

Summarize Candidate 3.

Which candidate has the best projects?

Which resume mentions Python?

Generate interview questions for Candidate 2.

Answer ONLY that question.

Do NOT generate the entire ATS report unless requested.

Never make up information.

If the answer is unavailable in the uploaded documents, reply:

"The uploaded documents do not contain that information."

Return Markdown.
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "success": True,
        "analysis": response.choices[0].message.content
    }
    # =====================================================
# Chat with Uploaded Documents
# =====================================================

@app.post("/chat")
def chat(request: ChatRequest):

    # Load Job Description
    jd_text = load_job_description()

    if jd_text is None:
        return {
            "success": False,
            "error": "Please upload a Job Description first."
        }

    # Load Resumes
    resumes = load_all_resumes()

    if resumes is None:
        return {
            "success": False,
            "error": "Please upload resumes first."
        }

    prompt = f"""
You are HireMate AI, an intelligent AI Recruiter.

You must answer ONLY using the uploaded Job Description and Candidate Resumes.

==================================================
JOB DESCRIPTION
==================================================

{jd_text}

==================================================
CANDIDATE RESUMES
==================================================

{resumes}

==================================================
USER QUESTION
==================================================

{request.message}

==================================================
INSTRUCTIONS
==================================================

Answer the user's question using ONLY the uploaded documents.

Examples:
- Who is the best candidate?
- Rank all candidates.
- Which candidate has AWS certification?
- Which candidate has React experience?
- Compare Candidate A and Candidate B.
- Summarize Candidate X.
- Which candidates satisfy the JD?
- Generate interview questions for Candidate Y.

Do not invent information.

If the answer is not available in the uploaded Job Description or resumes, reply:

"The uploaded documents do not contain that information."

Format the response using Markdown with headings and bullet points where appropriate.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are HireMate AI, an AI recruiting assistant. "
                    "Answer only from the uploaded documents."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "success": True,
        "reply": response.choices[0].message.content
    }
    