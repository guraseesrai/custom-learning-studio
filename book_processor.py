import os
import json
import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import tiktoken

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("ERROR: OpenAI API Key is missing! Check your .env file location and format.")

# Initialize the language model (LLM)
llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=OPENAI_API_KEY)

# Define token limits for context and scripts
MAX_CONTEXT_TOKENS = 1500
MAX_SCRIPT_TOKENS = 1500

def count_tokens(text, model="gpt-4"):
    """Count the number of tokens in a text string using tiktoken."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

def truncate_to_token_limit(text, token_limit, model="gpt-4"):
    """Truncate text so that it doesn't exceed the token limit."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) > token_limit:
        tokens = tokens[:token_limit]
        text = encoding.decode(tokens)
    return text

def extract_text_from_book(pdf_path):
    """Loads a PDF book and splits it into structured text chunks."""
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        return [chunk.page_content for chunk in chunks]  # Extract text content
    except Exception as e:
        return f"Error loading PDF: {str(e)}"

def generate_scripts(learning_outcomes, text_chunks):
    """
    For each learning outcome, generate a structured script using the first few text chunks as context.
    The context and resulting script are truncated to stay within token limits.
    The scripts are also saved as a JSON file.
    """
    scripts = {}

    # Prepare context from the first three chunks
    extracted_text = "\n\n".join(text_chunks[:3])
    extracted_text = truncate_to_token_limit(extracted_text, MAX_CONTEXT_TOKENS, model="gpt-4")

    for outcome in learning_outcomes:
        prompt = f"""
Generate a structured script for this learning outcome: {outcome}
Based on the following content:
{extracted_text}
"""
        response = llm.invoke(prompt)
        script_text = response if isinstance(response, str) else response.content  # Ensure text format
        script_text = truncate_to_token_limit(script_text, MAX_SCRIPT_TOKENS, model="gpt-4")
        scripts[outcome] = script_text

    # Save the scripts dictionary to a JSON file
    with open("scripts.json", "w") as f:
        json.dump(scripts, f, indent=2)
    
    return scripts

def generate_human_readable_articles(scripts):
    """
    Converts each structured script into four human-readable articles using different styles.
    Each prompt uses a truncated version of the script to remain within token limits.
    """
    articles = {}
    
    # Define four format styles with their respective instructions
    format_prompts = {
        "summary": "Summarize the script into a concise and informative article.",
        "blog": "Write an engaging blog post based on the script.",
        "detailed": "Expand the script into a detailed academic-style article.",
        "technical": "Convert the script into a technical document with clear and precise explanations."
    }

    for outcome, script in scripts.items():
        articles[outcome] = {}
        # Truncate script to ensure the prompt stays within the token limit
        script_truncated = truncate_to_token_limit(script, MAX_SCRIPT_TOKENS, model="gpt-4")
        for fmt, prompt_prefix in format_prompts.items():
            prompt = f"""
{prompt_prefix}
{script_truncated}
"""
            response = llm.invoke(prompt)
            article_text = response if isinstance(response, str) else response.content  # Ensure text format
            articles[outcome][fmt] = article_text
    return articles

def upload_file_to_s3(file_path, bucket_name, folder):
    """
    Uploads a file to an S3 bucket inside a specified folder.
    
    :param file_path: Local path to the file.
    :param bucket_name: Name of your S3 bucket.
    :param folder: Folder name in the bucket where the file will be stored.
    """
    # Construct the object key with the folder name
    object_name = f"{folder}/{os.path.basename(file_path)}"
    
    # Specify the correct region (e.g., 'us-west-2' for Oregon)
    s3_client = boto3.client('s3', region_name='us-west-2')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise e

# Example usage: store "scripts.json" in the "generated" folder
upload_file_to_s3("scripts.json", "seedstore", folder="scripts")

if __name__ == "__main__":
    # Example usage: specify a PDF file path and a list of learning outcomes.
    pdf_file_path = "path/to/your/book.pdf"  # Update with your PDF file path
    learning_outcomes = ["Learning Outcome 1", "Learning Outcome 2"]  # Update with your desired outcomes

    # Extract text from the PDF book
    text_chunks = extract_text_from_book(pdf_file_path)
    
    if isinstance(text_chunks, str) and text_chunks.startswith("Error"):
        print(text_chunks)
    else:
        # Generate structured scripts for each learning outcome
        scripts = generate_scripts(learning_outcomes, text_chunks)
        
        # Optionally, generate human-readable articles based on the scripts
        articles = generate_human_readable_articles(scripts)
        
        # Upload the generated JSON file to AWS S3
        s3_bucket = "seedstore"  # Replace with your actual S3 bucket name
        json_file_path = "scripts.json"
        upload_file_to_s3(json_file_path, s3_bucket, folder="scripts")

