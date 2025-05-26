from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
import os
import pathlib
import io
import json

from book_processor import extract_text_from_book, generate_scripts, generate_human_readable_articles, upload_file_to_s3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_word(file_path: str):
    try:
        import docx
    except ImportError:
        return "Error: python-docx not installed. Run 'pip install python-docx'."
    try:
        doc = docx.Document(file_path)
        full_text = "\n".join([p.text for p in doc.paragraphs])
        return [full_text]
    except Exception as e:
        return f"Error reading Word document: {str(e)}"

@app.post("/generate_seed/")
async def generate_seed(
    file: UploadFile = File(...),
    learning_outcomes: list[str] = Form(...),
):
    # Save the uploaded file locally
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Determine file type and extract text
    ext = pathlib.Path(file.filename).suffix.lower()
    if ext == ".pdf":
        text_chunks = extract_text_from_book(file_path)
    elif ext in [".doc", ".docx"]:
        text_chunks = extract_text_from_word(file_path)
    else:
        return {"error": "Unsupported file type. Please upload a PDF or Word document."}

    if isinstance(text_chunks, str) and text_chunks.startswith("Error"):
        return {"error": text_chunks}

    # Generate the seed scripts based on learning outcomes
    scripts = generate_scripts(learning_outcomes, text_chunks)
    
    # Save the seed scripts to a local JSON file
    json_file_path = "seed_scripts.json"
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(scripts, f, indent=2)

    # Upload the JSON file to S3 (for example, to a folder named "seed")
    s3_bucket = "seedstore"  # replace with your bucket name
    upload_file_to_s3(json_file_path, s3_bucket, folder="seed")
    
    # Optionally, construct the S3 URL to return
    s3_url = f"https://{s3_bucket}.s3.YOUR_REGION.amazonaws.com/seed/{os.path.basename(json_file_path)}"
    
    return {"message": "Seed script generated and stored in S3", "s3_url": s3_url}

