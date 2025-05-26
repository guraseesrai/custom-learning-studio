# 🎓 Custom Learning Studio

**Custom Learning Studio** is an interactive, AI-powered tool designed to generate structured learning scripts from PDF or Word documents based on user-defined learning outcomes. Built with **FastAPI**, **LangChain**, and **OpenAI GPT-4**, the system features a sleek frontend powered by **Bootstrap 5** and includes animations, dark mode, and downloadable results.

---

## ✨ Key Features

- 🤖 AI-generated content using GPT-4 via LangChain
- 📄 Upload `.pdf` or `.docx` to extract book content
- 🎯 Input learning outcomes and get auto-generated structured scripts
- 💾 Download results instantly as a `JSON` file
- 🎉 Animated UI with confetti, dark mode, and live stats
- ☁️ Optional cloud backup to AWS S3

---

## 🧱 Project Structure

custom_learning_studio/
├── main.py # FastAPI backend API

├── book_processor.py # PDF/Word parsing & GPT-4 integration

├── llm_service.py # OpenAI API call logic

├── templates/

│ └── index.html # Responsive UI (Bootstrap 5)

├── static/

│ ├── script.js # Frontend logic (JS)

│ └── styles.css # Theme styles (CSS)

├── uploads/ # Temporary file storage

├── seed_scripts.json # Generated script output

├── requirements.txt # Project dependencies

├── .env # Environment variables

└── key.env # Redundant key storage (not required)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/custom_learning_studio.git
cd custom_learning_studio
