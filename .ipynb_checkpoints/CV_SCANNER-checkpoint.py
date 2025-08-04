


get_ipython().system('pip install PyPDF2 spacy matplotlib pandas scikit-learn requests beautifulsoup4')
get_ipython().system('python -m spacy download en_core_web_sm')





import PyPDF2
import spacy
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer





def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text





nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text.lower())
    skills = []
    skill_keywords = ['python', 'java', 'sql', 'excel', 'machine learning', 'data analysis',
                      'communication', 'leadership', 'project management', 'cloud', 'aws', 'azure']
    for token in doc:
        if token.text in skill_keywords:
            skills.append(token.text)
    return list(set(skills))




def suggest_upskills(extracted_skills):
    all_skills = ['python', 'java', 'sql', 'excel', 'machine learning', 'data analysis',
                  'communication', 'leadership', 'project management', 'cloud', 'aws', 'azure']
    missing_skills = [skill for skill in all_skills if skill not in extracted_skills]
    return missing_skills





def fetch_youtube_links(skill):
    query = f"{skill} tutorial site:youtube.com"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href and "youtube.com/watch" in href:
            links.append(href.split("&")[0].replace("/url?q=", ""))
    return links[:3]  # Top 3 links





def calculate_ats_score(text, job_description):
    vectorizer = CountVectorizer().fit([text, job_description])
    vectors = vectorizer.transform([text, job_description])
    score = (vectors[0].multiply(vectors[1])).sum()
    total = vectors[1].sum()
    ats_score = round((score / total) * 100, 2)
    return ats_score





def generate_chart(skills, missing_skills, ats_score):
    labels = ['Skills Present', 'Skills Missing']
    values = [len(skills), len(missing_skills)]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title(f'Resume Analysis (ATS Score: {ats_score}%)')
    plt.ylabel('Number of Skills')
    plt.show()





pip install streamlit





jupyter nbconvert --to script CV_SCANNER.ipynb







