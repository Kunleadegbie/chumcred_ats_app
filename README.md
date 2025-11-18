# 📄 Chumcred ATS — AI-Powered Resume Screening System
Built with Streamlit • Python • TF-IDF • Hybrid Semantic Engine

Chumcred ATS is an AI-driven Applicant Tracking System (ATS) designed to help HR teams automatically evaluate applicant CVs against job descriptions using a combination of:

Keyword Matching

TF-IDF Similarity Analysis

Mini Semantic Scoring

Weighted Hybrid Model for Final Ranking

This system allows HR departments to upload multiple CVs along with a job description, and instantly receive:

Candidate Match Score

Keyword Match Percentage

TF-IDF Similarity Score

Mini Semantic Match Score

Final Ranking of All Applicants

Downloadable Excel Report

🚀 Features

✔ Upload unlimited CVs (PDF & DOCX)
✔ Upload or paste job descriptions
✔ Hybrid ATS scoring engine
✔ Ranked applicant shortlist
✔ Score explanation panel
✔ Download Excel report
✔ Optional Supabase integration for cloud storage
✔ Lightweight & Streamlit Cloud friendly

📁 Project Structure
chumcred_ats_app/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── helpers/
│   ├── cv_parser.py
│   ├── jd_processor.py
│   ├── matcher.py
│   ├── report_generator.py
│
├── config/
│   └── supabase_config.py (optional)
│
├── assets/
│   └── logo.png
│
└── data/
    ├── uploads/   (ignored by Git)
    ├── results/   (ignored by Git)
    └── sample/    (ignored by Git)


🔒 Note: The data/ directory is intentionally ignored using .gitignore to protect sample CVs and uploaded resumes.

🛠 Installation & Setup

Clone the repository:

git clone https://github.com/<your-username>/chumcred_ats_app.git
cd chumcred_ats_app


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py

☁️ Deploying on Streamlit Cloud

Push this repo to GitHub

Visit https://streamlit.io/cloud

Click New App

Select this repository

Add your secrets.toml (if using Supabase):

SUPABASE_URL="..."
SUPABASE_KEY="..."
SUPABASE_BUCKET="..."


Deploy 🚀

📊 How ATS Scoring Works
Score Type	Meaning
Match Score (%)	Final combined score indicating suitability
Keyword Match (%)	Number of JD keywords found in the CV
TF-IDF Score (%)	Similarity of CV text to JD text
Mini Semantic (%)	How similar the meaning is using light semantic mapping

The hybrid model balances accuracy with performance for Streamlit Cloud deployments.

🤝 Contributing

Feel free to fork this project and submit pull requests.
Suggestions and improvements are welcome.

📬 Author

Chumcred Limited
Dr. Adekunle Adegbie
AI · HR Technology · Data Solutions