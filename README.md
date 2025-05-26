# 🎓 Custom Learning Studio

**Custom Learning Studio** is an interactive, AI-powered tool that generates structured learning scripts from PDF or Word documents based on user-defined learning outcomes. Built with **FastAPI**, **LangChain**, and **OpenAI GPT-4**, the app ships with a modern **Bootstrap 5** frontend featuring dark mode, confetti animation, live stats, and instant JSON downloads.

---

## ✨ Key Features

- 🤖 AI-generated content using GPT-4 via LangChain  
- 📄 Upload **`.pdf`** or **`.docx`** files to extract book/course content  
- 🎯 Enter learning outcomes and receive auto-generated structured scripts  
- 💾 Download results instantly as a **`JSON`** file  
- 🎉 Animated UI with confetti, dark-mode toggle, and live counters  
- ☁️ Optional cloud backup to AWS S3  

---

## 🧱 Project Structure

```text
custom_learning_studio/
├── main.py               # FastAPI backend
├── book_processor.py     # PDF/Word parsing & GPT-4 prompts
├── llm_service.py        # OpenAI API helper
├── templates/
│   └── index.html        # Bootstrap 5 frontend
├── static/
│   ├── script.js         # Frontend logic
│   └── styles.css        # Theme styles (dark/light)
├── uploads/              # Temporary file storage
├── seed_scripts.json     # Example generated output
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── key.env               # (optional) backup key storage
