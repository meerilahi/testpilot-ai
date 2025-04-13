# 🧠 AI-Powered Exam System

An AI-driven platform that generates question papers based on the syllabus and automatically grades students' scanned answer sheets using NLP, OCR, and machine learning techniques.

---

## 🚀 Features

- 📄 **Automatic Question Paper Generation**
  - Generate custom question papers based on subject syllabus and topic distribution.

- 🧠 **Intelligent Answer Sheet Grading**
  - Extract answers from scanned sheets using OCR.
  - Use AI to grade short and long answers based on model answers or rubrics.
  - MCQ scoring via direct answer mapping.

- 📊 **Customizable Marking System**
  - Define marking criteria, partial scoring rules, and weightages.

- 💬 **Feedback Generation**
  - Provide meaningful feedback on student responses to help them improve.

- 📈 **Analytics Dashboard (Planned)**
  - Overview of class performance, average scores, and difficulty analysis.

---

## 🛠️ Technologies Used

- **Python** (Core)
- **FastAPI / Flask** (Backend API)
- **PyTorch / Transformers** (LLMs for grading)
- **Tesseract / PaddleOCR** (OCR Engine)
- **spaCy / NLTK / Scikit-learn** (NLP tasks)
- **React / HTML-CSS** (Frontend - optional)
- **PostgreSQL / SQLite** (Storage)

---

## 📁 Project Structure

```bash
ai-exam-system/
│
├── backend/                   # FastAPI/Flask application
│   └── grading/               # AI-based grading modules
│
├── ocr/                       # OCR preprocessing and extraction
│
├── models/                    # Saved ML/LLM models
│
├── data/                      # Sample answer sheets and questions
│
├── notebooks/                 # Experiments and evaluation notebooks
│
├── frontend/ (optional)       # UI code if building a dashboard
│
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview
