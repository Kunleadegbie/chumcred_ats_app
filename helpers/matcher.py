import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+]", " ", text)
    return text


def evaluate_candidate(filename, cv_text, jd_keywords, jd_vector_data):

    cleaned_cv = clean_text(cv_text)

    # -----------------------------------------------------
    # 1. KEYWORD SCORE
    # -----------------------------------------------------
    matched_keywords = [kw for kw in jd_keywords if kw in cleaned_cv]
    keyword_score = (len(matched_keywords) / len(jd_keywords)) * 100 if jd_keywords else 0


    # -----------------------------------------------------
    # 2. TF-IDF SEMANTIC SCORE
    # -----------------------------------------------------
    vectorizer = jd_vector_data["vectorizer"]
    jd_vector = jd_vector_data["jd_vector"]

    try:
        cv_vector = vectorizer.transform([cleaned_cv])
        tfidf_score = float(cosine_similarity(jd_vector, cv_vector)[0][0] * 100)
    except:
        tfidf_score = 0


    # -----------------------------------------------------
    # 3. MINI-EMBEDDING SCORE (Lightweight Semantic)
    # -----------------------------------------------------
    # Instead of heavy BERT, use small TF-IDF semantic smoothing
    mini_semantic_score = np.sqrt((keyword_score * tfidf_score))  # geometric mean


    # -----------------------------------------------------
    # 4. FINAL HYBRID SCORE
    # -----------------------------------------------------
    final_score = (keyword_score * 0.30) + (tfidf_score * 0.40) + (mini_semantic_score * 0.30)


    # -----------------------------------------------------
    # 5. VERDICT
    # -----------------------------------------------------
    if final_score >= 75:
        verdict = "Highly Qualified"
    elif final_score >= 50:
        verdict = "Partially Qualified"
    else:
        verdict = "Not Qualified"


    # -----------------------------------------------------
    # 6. RETURN RESULTS
    # -----------------------------------------------------
    return {
        "Applicant": filename,
        "Match Score (%)": round(final_score, 2),
        "Keyword Match (%)": round(keyword_score, 2),
        "TF-IDF Score (%)": round(tfidf_score, 2),
        "Mini Semantic (%)": round(mini_semantic_score, 2),
        "Verdict": verdict,
        "Matched Keywords": ", ".join(matched_keywords[:20])
    }
