import PyPDF2
import spacy
import torch
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import textstat

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_skills(text):
    doc = nlp(text.lower())
    skill_keywords = ['python', 'java', 'sql', 'excel', 'machine learning', 'data analysis',
                      'communication', 'leadership', 'project management', 'cloud', 'aws', 'azure']
    skills = [token.text for token in doc if token.text in skill_keywords]
    return list(set(skills))


def skill_frequency(text, skill_keywords):
    words = text.lower().split()
    freq = Counter(word for word in words if word in skill_keywords)
    return dict(freq)


def suggest_upskills(extracted_skills, all_skills):
    return [skill for skill in all_skills if skill not in extracted_skills]


def extract_entities(text):
    doc = nlp(text)
    entities = {
        "ORG": set(),
        "PERSON": set(),
        "GPE": set(),
        "EDUCATION": set()
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text)
        elif ent.label_ == "NORP" or ent.label_ == "FAC":
            entities["EDUCATION"].add(ent.text)
    return {k: list(v) for k, v in entities.items()}


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
    return links[:3]


def calculate_ats_score(text, job_description):
    vectorizer = CountVectorizer().fit([text, job_description])
    vectors = vectorizer.transform([text, job_description])
    score = (vectors[0].multiply(vectors[1])).sum()
    total = vectors[1].sum()
    ats_score = round((score / total) * 100, 2)
    return ats_score


def analyze_readability(text):
    return {
        "word_count": len(text.split()),
        "flesch_score": textstat.flesch_reading_ease(text),
        "grade_level": textstat.text_standard(text)
    }


def rank_missing_skills(missing_skills, job_description):
    job_text = job_description.lower()
    severity = {}
    for skill in missing_skills:
        count = job_text.count(skill.lower())
        severity[skill] = count
    ranked = sorted(severity.items(), key=lambda x: x[1], reverse=True)
    return ranked


def generate_chart(skills, missing_skills, ats_score):
    labels = ['Skills Present', 'Skills Missing']
    values = [len(skills), len(missing_skills)]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title(f'Resume Analysis (ATS Score: {ats_score}%)')
    plt.ylabel('Number of Skills')
    plt.tight_layout()
    plt.show()


def generate_report(text, job_description):
    all_skills = ['python', 'java', 'sql', 'excel', 'machine learning', 'data analysis',
                  'communication', 'leadership', 'project management', 'cloud', 'aws', 'azure']
    skills = extract_skills(text)
    missing = suggest_upskills(skills, all_skills)
    ats = calculate_ats_score(text, job_description)
    freq = skill_frequency(text, all_skills)
    entities = extract_entities(text)
    readability = analyze_readability(text)
    severity = rank_missing_skills(missing, job_description)

    return {
        "skills_present": skills,
        "skills_missing": missing,
        "ats_score": ats,
        "skill_frequency": freq,
        "named_entities": entities,
        "readability": readability,
        "missing_skill_severity": severity
    }
