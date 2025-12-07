import streamlit as st
from resume_parser import parse_resume
from embeddings import train_fasttext, get_doc_vector
from ranker import rank
from report import generate_report

st.title("AI Resume Screening & Ranking System")

job = st.file_uploader("Upload Job Description (PDF/TXT)", type=["pdf", "txt"])
resumes = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if st.button("Process & Rank"):

    all_tokens = []
    resume_tokens = []
    resume_names = []

    # --- JOB DESCRIPTION ---
    if not job:
        st.error("Please upload a job description.")
        st.stop()

    job_path = "job_desc.pdf"
    with open(job_path, "wb") as f:
        f.write(job.getbuffer())

    job_text, job_tok = parse_resume(job_path)
    all_tokens.append(job_tok)

    # --- RESUMES ---
    for r in resumes:
        path = r.name
        with open(path, "wb") as f:
            f.write(r.getbuffer())
        txt, tok = parse_resume(path)
        resume_tokens.append(tok)
        resume_names.append(r.name)
        all_tokens.append(tok)

    # Remove empty token lists
    all_tokens = [x for x in all_tokens if len(x) > 0]

    if len(all_tokens) < 2:
        st.error("Not enough readable text found. One or more PDFs may be scanned or empty.")
        st.stop()

    model = train_fasttext(all_tokens)

    job_vec = get_doc_vector(job_tok, model)
    resume_vecs = [get_doc_vector(x, model) for x in resume_tokens]

    results = rank(job_vec, resume_vecs, resume_names)

    st.subheader("Ranking Results")
    for score, name in results:
        st.write(f"**{name}** — Score: {score:.3f}")

    path = generate_report(results)
    st.download_button("Download Report", open(path, "rb"), "report.html")
