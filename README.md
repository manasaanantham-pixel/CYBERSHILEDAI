# 🛡️ CyberShield-AI

### AI-Powered Malware & Email Threat Detection Platform

CyberShield-AI is an AI-powered cybersecurity platform designed to detect **malware, phishing, spam, and suspicious email content** using machine learning and intelligent security analysis.

The platform provides a centralized dashboard where users can upload files for malware detection and connect their Gmail account to analyze emails for potential security threats.

---

## 🚀 Features

### 🔐 User Authentication

* User registration and login
* Secure password hashing
* Authentication-based dashboard access

### 🦠 AI-Powered Malware Detection

* Upload suspicious files for analysis
* Machine-learning-based malware classification
* Threat status detection
* Confidence score for predictions
* Supports automated file feature extraction

### 📧 Gmail Security Analysis

* Connect Gmail securely using Google OAuth
* Retrieve email messages
* Analyze email content
* Detect potential phishing and spam
* Identify suspicious messages
* Display risk level and confidence

### 📊 Security Dashboard

* Total emails analyzed
* Malware detections
* Phishing detections
* Spam detections
* Safe messages
* Threat summary and statistics

### 📝 Scan History

* Maintain previous analysis results
* Track detected threats
* View file/email analysis information

### 🎨 Modern Cybersecurity UI

* Dark cybersecurity-themed interface
* Responsive React frontend
* Modern dashboard
* Glassmorphism-inspired components
* Security-focused visual design

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Frontend     │
                    │      Dashboard       │
                    └──────────┬───────────┘
                               │
                         REST API / HTTP
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌─────────────┐   ┌─────────────┐
       │ Malware ML │   │ Gmail API   │   │ Database    │
       │   Model    │   │   Service   │   │             │
       └─────┬──────┘   └──────┬──────┘   └─────────────┘
             │                 │
             ▼                 ▼
       File Analysis      Email Analysis
             │                 │
             └────────┬────────┘
                      ▼
             ┌──────────────────┐
             │ Threat Detection │
             │      Result      │
             └──────────────────┘
```

---

# 🔄 Application Workflow

```text
User
  │
  ├── Login / Signup
  │
  ▼
Dashboard
  │
  ├── Upload File
  │      │
  │      ▼
  │   Feature Extraction
  │      │
  │      ▼
  │   ML Model
  │      │
  │      ▼
  │   Malware / Safe
  │
  └── Connect Gmail
         │
         ▼
      Gmail API
         │
         ▼
     Fetch Emails
         │
         ▼
    Email Analysis
         │
         ▼
   Phishing / Spam /
   Safe / Suspicious
```

---

# 🧠 Machine Learning

CyberShield-AI uses machine learning models to identify potential security threats.

## Malware Detection

The malware detection component uses a **Random Forest Classifier** trained on malware-related features.

### Model Pipeline

```text
Input File
    ↓
Feature Extraction
    ↓
Feature Preprocessing
    ↓
Random Forest Model
    ↓
Prediction
    ↓
Threat Classification
```

The model generates a prediction along with a confidence score to help the user understand the detected threat level.

### Example Result

```text
File: suspicious.exe

Prediction: Malware
Status: Danger
Confidence: 77.0%
```

---

# 📧 Email Security

The Gmail security module integrates with the **Gmail API** to retrieve and analyze email messages.

The system can classify suspicious emails based on their content and security characteristics.

### Example classifications

* ✅ Safe
* ⚠️ Suspicious
* 🚨 Phishing
* 🛑 Spam

### Email Analysis Workflow

```text
Gmail Account
      ↓
Google OAuth Authentication
      ↓
Gmail API
      ↓
Email Retrieval
      ↓
Text / Content Analysis
      ↓
ML Security Model
      ↓
Threat Classification
```

---

# 🛠️ Technologies Used

## Frontend

* React.js
* Vite
* JavaScript
* HTML5
* CSS3
* REST API

## Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic

## Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

## Security & APIs

* Gmail API
* Google OAuth 2.0
* Password Hashing
* CORS

## Database

* SQLite / SQLAlchemy

## Development Tools

* Visual Studio Code
* Git
* GitHub
* Postman
* Google Cloud Console

---

# 📂 Project Structure

```text
CyberShield-AI/
│
├── backend/
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   │
│   ├── gmail/
│   │   ├── google_oauth.py
│   │   ├── gmail_service.py
│   │   └── email_parser.py
│   │
│   ├── ml/
│   │   ├── malware_model.pkl
│   │   ├── features.pkl
│   │   ├── email_security_model.pkl
│   │   ├── predictor.py
│   │   └── pe_features.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── gmail.py
│   │   └── analysis.py
│   │
│   ├── services/
│   │   ├── predict.py
│   │   ├── train.py
│   │   └── feature_extractor.py
│   │
│   ├── uploads/
│   ├── history/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── Auth.jsx
│   │   ├── Auth.css
│   │   ├── Dashboard.jsx
│   │   └── Dashboard.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── dataset/
│
├── documentation/
│
├── presentation/
│
├── demo/
│
├── .gitignore
└── README.md
```

> **Note:** The exact folder structure may vary depending on the final project version.

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/CyberShield-AI.git
```

Move into the project:

```bash
cd CyberShield-AI
```

---

# ⚙️ Backend Setup

Open a terminal and navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./cybershield.db
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

⚠️ **Never upload your real `.env` file, Google credentials, OAuth tokens, API keys, or passwords to GitHub.**

Create a `.gitignore` file and add:

```gitignore
venv/
__pycache__/
.env
*.db
*.sqlite
token.json
credentials.json
uploads/
history/
*.pkl
```

If your project requires the trained model files to run, keep the required model files in the repository or provide a secure download/setup method instead of blindly ignoring them.

---

# ▶️ Run the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The backend should run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Frontend Setup

Open another terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will usually be available at:

```text
http://localhost:5173
```

If Vite selects another port, use the URL shown in the terminal.

---

# 🔐 Gmail API Configuration

To enable Gmail analysis:

1. Open Google Cloud Console.
2. Create or select a Google Cloud project.
3. Enable the Gmail API.
4. Configure the OAuth consent screen.
5. Create OAuth credentials.
6. Configure the required redirect URI.
7. Add the required credentials to your local environment.
8. Start the CyberShield-AI backend.
9. Connect Gmail from the application dashboard.

For security reasons, **OAuth credentials and tokens must never be committed to GitHub.**

---

# 📊 Example Detection Results

## Malware Detection

```text
┌─────────────────────────────────┐
│ File: suspicious.exe            │
│                                 │
│ Prediction: Malware             │
│ Status: Danger                  │
│ Confidence: 77.0%               │
└─────────────────────────────────┘
```

## Email Detection

```text
┌─────────────────────────────────┐
│ Email: Security Alert           │
│                                 │
│ Prediction: Phishing            │
│ Risk Level: High                │
│ Confidence: 43.4%               │
└─────────────────────────────────┘
```

---

# 🎯 Objectives

The main objectives of CyberShield-AI are:

1. Develop an AI-based malware detection system.
2. Detect suspicious and malicious files automatically.
3. Analyze emails for phishing and spam threats.
4. Provide users with understandable security results.
5. Build a centralized cybersecurity dashboard.
6. Improve awareness of potential digital threats.

---

# 👥 Target Users

CyberShield-AI can be useful for:

* Students
* Individual users
* Small organizations
* Security learners
* IT administrators
* Cybersecurity beginners

---

# 🔒 Security Considerations

CyberShield-AI is designed as an educational cybersecurity project.

Important security practices include:

* Never expose API keys.
* Never commit OAuth credentials.
* Never commit passwords.
* Never commit access tokens.
* Validate uploaded files.
* Restrict file upload types and sizes.
* Use HTTPS in production.
* Use secure authentication mechanisms.
* Store sensitive configuration in environment variables.

---

# 📈 Future Enhancements

Future versions could include:

* Real-time threat monitoring
* Advanced phishing URL detection
* Browser extension
* URL reputation checking
* Attachment sandbox analysis
* YARA rule integration
* Threat intelligence APIs
* Multi-model malware detection
* Explainable AI predictions
* Security alerts and notifications
* Cloud deployment
* Role-based access control
* Advanced analytics and reports

---

# 🧪 Testing

The application should be tested for:

### Authentication

* User registration
* Login
* Invalid credentials
* Session handling

### Malware Detection

* Safe files
* Suspicious files
* Malicious samples
* Invalid file formats

### Gmail Analysis

* Gmail authentication
* Email retrieval
* Phishing detection
* Spam detection
* Safe email classification

### API

* Authentication endpoints
* Upload endpoints
* Prediction endpoints
* Gmail endpoints
* Analysis endpoints

---

# 📸 Screenshots

DOC LINK:
https://docs.google.com/document/d/1b6F3Zh1AJDVm83fqTgnSvYBw59YQDDLI/edit?usp=drive_link&ouid=118266643788459243835&rtpof=true&sd=true

![Login](docs/login.png)

![Dashboard](docs/dashboard.png)

![Malware Detection](docs/malware-detection.png)

![Gmail Analysis](docs/gmail-analysis.png)
```

---

# 🎥 Demo

Add your project demonstration video link here:
Demo Video:
https://drive.google.com/file/d/1V4vE4itFUchIukiZ2qRaZE5pDDU8UMuW/view?usp=drive_link

# 📚 Project Documentation

The complete project documentation should contain:

* Introduction
* Problem Statement
* Objectives
* Existing System
* Proposed System
* System Architecture
* Module Description
* Technology Stack
* Database Design
* Machine Learning Methodology
* Implementation
* Testing
* Results
* Screenshots
* Limitations
* Future Scope
* Conclusion
* References

---

# 🏆 Project Highlights

### 🧠 Artificial Intelligence

Machine learning-based threat detection.

### 🛡️ Cybersecurity

Malware, phishing, and spam threat analysis.

### 📧 Email Security

Gmail integration for email threat detection.

### 📊 Analytics

Centralized dashboard for security insights.

### ⚡ Modern Architecture

React frontend + FastAPI backend + ML services.

---

# 👩‍💻 Developed By

**Manasa Anantham**

B.Tech – Data Science

**Malla Reddy Engineering College for Women, Hyderabad**
Mail iD :- manasaanantham@gmail.com
github link :- https://github.com/manasaanantham-pixel
---

# 📄 License

This project is developed for **educational and academic purposes**.

You may modify and extend the project for learning and research purposes.

---

# ⭐ Acknowledgements

This project uses open-source technologies and APIs including:

* Python
* FastAPI
* React
* Vite
* Scikit-learn
* Pandas
* NumPy
* SQLAlchemy
* Gmail API
* Google OAuth

---

## 🛡️ CyberShield-AI

> **Detect Threats. Protect Every File.**

A smarter approach to AI-powered cybersecurity.
