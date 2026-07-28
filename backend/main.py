import os

import json

from ats_engine import calculate_resume_score
import shutil
from typing import List

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq import Groq

from file_utils import extract_text
from resume_parser import parse_resume


# =====================================================
# Environment
# =====================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =====================================================
# FastAPI
# =====================================================

app = FastAPI(
    title="HireMate AI",
    version="2.0"
)


# =====================================================
# Directories
# =====================================================

os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/jd", exist_ok=True)
os.makedirs("uploads/resumes", exist_ok=True)
os.makedirs("parsed_data", exist_ok=True)

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
# Upload JD
# =====================================================

@app.post("/upload-jd")
async def upload_jd(
    file: UploadFile = File(...)
):

    filepath = os.path.join(
        "uploads",
        "jd",
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from JD
    text = extract_text(filepath)

    # Save extracted text for ATS engine
    with open("uploads/jd/jd.txt", "w", encoding="utf-8") as f:
        f.write(text)

    return {
        "success": True,
        "filename": file.filename
    }


# =====================================================
# Upload Resumes
# =====================================================

@app.post("/upload-resumes")
async def upload_resumes(
    files: List[UploadFile] = File(...)
):

    uploaded = []

    for file in files:

        filepath = os.path.join(
            "uploads",
            "resumes",
            file.filename
        )

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(filepath)

        parsed = parse_resume(text)

        json_file = os.path.join(
            "parsed_data",
            file.filename.rsplit(".", 1)[0] + ".json"
        )

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4)

        uploaded.append(file.filename)

    return {
        "success": True,
        "uploaded": uploaded
    }


# =====================================================
# Calculate ATS
# =====================================================

@app.post("/calculate-ats")
async def calculate_ats():

    jd_path = "uploads/jd/jd.txt"

    if not os.path.exists(jd_path):
        raise HTTPException(
            status_code=400,
            detail="Please upload a Job Description first."
        )

    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    results = []

    for file in os.listdir("parsed_data"):

        if not file.endswith(".json"):
            continue

        with open(
            os.path.join("parsed_data", file),
            "r",
            encoding="utf-8"
        ) as f:
            resume = json.load(f)

        ats = calculate_resume_score(
            jd_text,
            resume.get("skills", []),
            resume.get("education", []),
            resume.get("experience", []),
            resume.get("projects", []),
            resume.get("certifications", [])
        )

        resume["ats_score"] = ats["ats_score"]
        resume["matched_skills"] = ats["matched_skills"]
        resume["missing_skills"] = ats["missing_skills"]

        resume["skill_score"] = ats["skill_score"]
        resume["education_score"] = ats["education_score"]
        resume["experience_score"] = ats["experience_score"]
        resume["project_score"] = ats["project_score"]
        resume["certification_score"] = ats["certification_score"]

        results.append(resume)

    results.sort(
        key=lambda x: x["ats_score"],
        reverse=True
    )

    return {
        "success": True,
        "results": results
    }




# =====================================================
# Recruiter Chat
# =====================================================

@app.post("/chat")
async def recruiter_chat(request: ChatRequest):

    candidates = []

    for file in os.listdir("parsed_data"):

        if file.endswith(".json"):

            with open(
                os.path.join("parsed_data", file),
                "r",
                encoding="utf-8"
            ) as f:

                candidates.append(json.load(f))

    prompt = f"""
You are an AI Recruiter.

Candidate Database:

{json.dumps(candidates, indent=2)}

Recruiter's Question:

{request.message}

Answer professionally.
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
        "answer": response.choices[0].message.content
    }


# =====================================================
# Candidate Details API
# =====================================================

@app.get("/candidate/{candidate_name}")
async def get_candidate(candidate_name: str):

    for file in os.listdir("parsed_data"):

        if not file.endswith(".json"):
            continue

        path = os.path.join("parsed_data", file)

        with open(path, "r", encoding="utf-8") as f:
            candidate = json.load(f)

        if candidate.get("candidate", "").lower() == candidate_name.lower():
            return candidate

    raise HTTPException(
        status_code=404,
        detail="Candidate not found"
    )