import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+]", " ", text)
    return text


def process_job_description(jd_text):
    """
    1. Clean JD
    2. Extract keywords
    3. Create TF-IDF vector for JD
    """

    cleaned_jd = clean_text(jd_text)

    # Extract keywords
    keywords = list(set(re.findall(r"[a-zA-Z]{3,}", cleaned_jd)))

    # Prepare TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english")
    jd_vector = vectorizer.fit_transform([cleaned_jd])

    return keywords, {
        "vectorizer": vectorizer,
        "jd_vector": jd_vector
    }
