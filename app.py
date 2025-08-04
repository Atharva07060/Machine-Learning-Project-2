from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import os
import textstat
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
nlp = spacy.load("en_core_web_sm")

job_keywords = {
    "Data Scientist": ["Python", "Machine Learning", "Statistics", "Pandas", "SQL", "Communication"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git", "Responsive Design"],
    "AI Engineer": ["Python", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Model Deployment"]
}

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def calculate_ats_score(text, keywords):
    score = sum(1 for kw in keywords if kw.lower() in text.lower())
    return int((score / len(keywords)) * 100)

def suggest_upskilling(text, keywords):
    return [kw for kw in keywords if kw.lower() not in text.lower()]

def fetch_youtube_links(skills, max_links=1):
    tutorial_links = {}
    for skill in skills:
        query = skill + " tutorial"
        url = f"https://www.youtube.com/results?search_query={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        video_ids = []
        for script in soup.find_all("script"):
            if "videoId" in script.text:
                video_ids += [vid.split('"')[3] for vid in script.text.split('videoId') if '"' in vid]
        links = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids[:max_links]]
        tutorial_links[skill] = links
    return tutorial_links

def analyze_readability(text):
    return {
        "word_count": len(text.split()),
        "flesch_score": round(textstat.flesch_reading_ease(text), 2),
        "grade_level": textstat.text_standard(text)
    }

def extract_entities(text):
    doc = nlp(text)
    entities = {"ORG": set(), "GPE": set(), "EDUCATION": set()}
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["ORG"].add(ent.text)
        elif ent.label_ == "GPE":
            entities["GPE"].add(ent.text)
        elif ent.label_ in ["NORP", "FAC", "PERSON"]:
            entities["EDUCATION"].add(ent.text)
    return {k: list(v) for k, v in entities.items()}

def detect_sections(text):
    sections = ["Education", "Experience", "Skills", "Projects", "Certifications", "Summary"]
    found = [sec for sec in sections if sec.lower() in text.lower()]
    return found

def generate_report(data):
    report = f"""
Resume Analysis Report
----------------------
Job Role: {data['role']}
ATS Score: {data['ats_score']} / 100
Word Count: {data['readability']['word_count']}
Flesch Reading Ease: {data['readability']['flesch_score']}
Grade Level: {data['readability']['grade_level']}

Sections Found: {', '.join(data['sections'])}
Missing Skills: {', '.join(data['missing_skills']) if data['missing_skills'] else 'None'}

Named Entities:
- Organizations: {', '.join(data['entities']['ORG'])}
- Locations: {', '.join(data['entities']['GPE'])}
- Education: {', '.join(data['entities']['EDUCATION'])}
"""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w")
    tmp.write(report)
    tmp.close()
    return tmp.name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        role = request.form.get("role")
        file = request.files.get("resume")

        if file and role:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            resume_text = extract_text_from_pdf(file_path)
            keywords = job_keywords.get(role, [])
            ats_score = calculate_ats_score(resume_text, keywords)
            missing_skills = suggest_upskilling(resume_text, keywords)
            tutorials = fetch_youtube_links(missing_skills)
            readability = analyze_readability(resume_text)
            entities = extract_entities(resume_text)
            sections = detect_sections(resume_text)

            report_data = {
                "role": role,
                "ats_score": ats_score,
                "readability": readability,
                "missing_skills": missing_skills,
                "entities": entities,
                "sections": sections
            }
            report_path = generate_report(report_data)

            return render_template("index.html",
                                   resume_text=resume_text,
                                   ats_score=ats_score,
                                   missing_skills=missing_skills,
                                   tutorials=tutorials,
                                   readability=readability,
                                   entities=entities,
                                   sections=sections,
                                   role=role,
                                   job_roles=list(job_keywords.keys()),
                                   report_path=report_path)
    return render_template("index.html", job_roles=list(job_keywords.keys()))

@app.route("/download")
def download():
    path = request.args.get("path")
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
