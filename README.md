# CvScanner:

## 📄 CVScanner - Resume Analysis and ATS Compatibility Tool

**CVScanner** is a Flask-based AI-powered resume analysis tool that evaluates resumes for **ATS (Applicant Tracking System) compatibility**, identifies **missing skills**, suggests **upskilling resources**, performs **readability analysis**, and extracts **key entities**—all from a single PDF upload. It is designed to assist job seekers in optimizing their resumes to improve selection chances in automated recruitment systems.

---

### 🚀 Key Features

* ✅ **ATS Score Evaluation**
  Automatically scores resumes based on keyword relevance, formatting, and structure, as used by modern ATS tools.

* 📌 **Missing Skills & Keywords Detection**
  Compares resume content against job-relevant skillsets and highlights what’s missing.

* 📚 **YouTube Tutorial Suggestions**
  Recommends personalized upskilling content from YouTube based on missing skills or technologies.

* 🧠 **Named Entity Recognition (NER)**
  Extracts essential resume entities like Name, Email, Phone Number, Designation, and Total Experience.

* 📖 **Readability Analysis**
  Evaluates the readability of the resume using Flesch Reading metrics to ensure clarity and professionalism.

* 📊 **Dashboard with Insights**
  Displays ATS score, extracted skills, readability score, and recommendations in an interactive UI.

---

### 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS, Bootstrap
* **NLP & ML**: spaCy, sklearn, Flesch Reading Ease
* **PDF Parsing**: PyMuPDF (fitz)
* **Visualization**: Matplotlib, WordCloud
* **API Integration**: YouTube Data API

---

### 📂 Folder Structure

```
CVScanner/
│
├── static/               # CSS, JS, Wordclouds
├── templates/            # HTML templates
├── resume_parser.py      # Resume entity extraction logic
├── skill_matcher.py      # Matching skills to job description
├── readability.py        # Readability scoring logic
├── youtube_fetcher.py    # Fetches YouTube tutorial links
├── app.py                # Main Flask app
├── requirements.txt      # Dependencies
└── README.md             # Project description
```

---

### 📌 How to Use

1. Clone the repository

   ```bash
   git clone https://github.com/<your-username>/CVScanner.git
   cd CVScanner
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask App

   ```bash
   python app.py
   ```

4. Open the app in your browser

   ```
   http://localhost:5000
   ```

5. Upload your resume PDF and get instant feedback!

---

### 📸 Sample Output

* ATS Score with Suggestions
* Readability Chart
* Word Cloud of Resume Skills
* List of Missing Skills with YouTube Links
* Entity Extraction Table

---

### 💡 Ideal For

* Students & Freshers improving their resumes
* Job seekers targeting specific roles
* Career counselors providing resume feedback
* Platforms offering resume analysis as a service

---

Let me know if you want a matching **project banner image**, **GIF demo**, or **badges** (e.g., Flask, Python, NLP).
