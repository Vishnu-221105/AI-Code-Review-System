# 🛡️ CodeGuard AI – Intelligent Python Code Review System

CodeGuard AI is an AI-powered Python code review application that analyzes source code, identifies potential errors, detects security vulnerabilities, and provides suggestions for improvement.

The application combines traditional Python analysis tools with an AI-based review system to help developers write cleaner, safer, and more maintainable code.

## 🚀 Features

- **Syntax Validation:** Detects Python syntax errors using Abstract Syntax Tree (AST) validation.
- **Code Quality Analysis:** Identifies coding standard and maintainability issues using Pylint.
- **Security Analysis:** Scans Python code for potentially unsafe patterns using Bandit.
- **AI-Powered Code Review:** Uses Groq to explain bugs, logical errors, and improvement opportunities.
- **Improved Code Suggestions:** Generates an improved version of submitted code.
- **Code Upload:** Supports uploading Python (`.py`) files.
- **Interactive Dashboard:** Displays analysis results in an organized Streamlit interface.
- **Download Improved Code:** Allows users to download the AI-generated code.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| AST | Syntax validation |
| Pylint | Code quality analysis |
| Bandit | Security analysis |
| Groq API | AI-powered code review |

## 🖥️ Application Workflow

1. Enter Python code or upload a `.py` file.
2. Select the required analysis options.
3. Start the code review.
4. The system performs syntax, quality, and security analysis.
5. Groq AI reviews the submitted code.
6. View the results and suggested improvements.
7. Download the improved code if available.

## 📂 Project Structure

```text
AI-Code-Review/
│
├── app.py
├── ai_reviewer.py
├── code_analyzer.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

**Note:** The `.env` file stores your API key locally and should never be uploaded to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vishnu-221105/AI-Code-Review-System.git
```

### 2. Open the project folder

```bash
cd AI-Code-Review-System
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project folder and add:

```text
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your own Groq API key.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at:

`http://localhost:8501`

## 🔐 Security Note

- Never share your Groq API key publicly.
- Keep the `.env` file out of version control.
- Submitted code is analyzed, not executed by the application.
- Security scan results should be reviewed before relying on them.

## 👨‍💻 Developer

**Vishnu R**

GitHub: [Vishnu-221105](https://github.com/Vishnu-221105)

## 📌 Project

**CodeGuard AI – Intelligent Python Code Analysis and Review System**

Built using Python, Streamlit, Pylint, Bandit, and Groq.