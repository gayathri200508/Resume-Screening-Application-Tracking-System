"""
app.py
------
Streamlit demo UI for the Resume Screening & Application Tracking System.

Run with:
    streamlit run app.py
"""

import os
import tempfile

import pandas as pd
import streamlit as st

from src.resume_parser import extract_text, clean_text
from src.skill_extractor import extract_candidate_profile
from src.matcher import evaluate_resume, rank_candidates
from src.tracker import (
    init_db,
    add_candidate,
    get_all_candidates,
    update_status,
    clear_all,
    STATUS_OPTIONS,
)

st.set_page_config(page_title="Resume Screening & ATS", page_icon="🧾", layout="wide")
init_db()

st.title("🧾 Resume Screening & Application Tracking System")
st.caption(
    "Upload a job description and a batch of resumes (PDF/DOCX). "
    "The system extracts skills using NLP, scores each resume against "
    "the job description, and ranks the candidates."
)

tab_screen, tab_track = st.tabs(["📋 Screen & Rank Resumes", "📊 Application Tracker"])

# -----------------------------------------------------------------------
# TAB 1 - Screening & Ranking
# -----------------------------------------------------------------------
with tab_screen:
    col_jd, col_resumes = st.columns(2)

    with col_jd:
        st.subheader("1. Job Description")
        job_title = st.text_input("Job Title", value="Python Developer")
        jd_text_input = st.text_area(
            "Paste the Job Description here",
            height=220,
            placeholder="e.g. We are looking for a Python developer skilled in "
            "Django, REST APIs, SQL, and Git...",
        )
        jd_file = st.file_uploader(
            "...or upload JD as PDF/DOCX (optional, overrides text above)",
            type=["pdf", "docx"],
            key="jd_file",
        )

    with col_resumes:
        st.subheader("2. Candidate Resumes")
        resume_files = st.file_uploader(
            "Upload one or more resumes (PDF or DOCX)",
            type=["pdf", "docx"],
            accept_multiple_files=True,
        )

    run = st.button("🚀 Screen & Rank Candidates", type="primary")

    if run:
        # Resolve JD text (uploaded file takes priority over pasted text)
        jd_text = jd_text_input
        if jd_file is not None:
            suffix = os.path.splitext(jd_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(jd_file.read())
                tmp_path = tmp.name
            jd_text = clean_text(extract_text(tmp_path))
            os.unlink(tmp_path)

        if not jd_text.strip():
            st.error("Please paste or upload a job description first.")
        elif not resume_files:
            st.error("Please upload at least one resume.")
        else:
            results = []
            with st.spinner("Extracting skills and scoring resumes..."):
                for rfile in resume_files:
                    suffix = os.path.splitext(rfile.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(rfile.read())
                        tmp_path = tmp.name

                    try:
                        raw_text = extract_text(tmp_path)
                        text = clean_text(raw_text)
                        profile = extract_candidate_profile(text)
                        evaluation = evaluate_resume(text, jd_text)

                        candidate = {
                            "filename": rfile.name,
                            "name": profile["name"],
                            "email": profile["email"],
                            "phone": profile["phone"],
                            "resume_skills": evaluation["resume_skills"],
                            "matched_skills": evaluation["matched_skills"],
                            "missing_skills": evaluation["missing_skills"],
                            "similarity_score": evaluation["similarity_score"],
                            "skill_match_score": evaluation["skill_match_score"],
                            "final_score": evaluation["final_score"],
                            "job_title": job_title,
                        }
                        results.append(candidate)
                    finally:
                        os.unlink(tmp_path)

            ranked = rank_candidates(results)

            st.success(f"Screened {len(ranked)} candidate(s) successfully!")
            st.subheader("🏆 Ranked Candidates")

            display_df = pd.DataFrame(
                [
                    {
                        "Rank": i + 1,
                        "Name": c["name"],
                        "Email": c["email"],
                        "Final Score": c["final_score"],
                        "Similarity %": c["similarity_score"],
                        "Skill Match %": c["skill_match_score"],
                        "Matched Skills": ", ".join(c["matched_skills"]) or "—",
                        "File": c["filename"],
                    }
                    for i, c in enumerate(ranked)
                ]
            )
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            with st.expander("🔍 View detailed skill breakdown per candidate"):
                for c in ranked:
                    st.markdown(f"**{c['name']}** ({c['filename']})")
                    colA, colB = st.columns(2)
                    colA.markdown("✅ **Matched Skills:** " + (", ".join(c["matched_skills"]) or "None"))
                    colB.markdown("❌ **Missing Skills:** " + (", ".join(c["missing_skills"]) or "None"))
                    st.divider()

            if st.button("💾 Save these results to Application Tracker"):
                for c in ranked:
                    add_candidate(c)
                st.success("Saved! Check the 'Application Tracker' tab.")

# -----------------------------------------------------------------------
# TAB 2 - Application Tracker
# -----------------------------------------------------------------------
with tab_track:
    st.subheader("📊 Application Tracker")
    st.caption("Track every screened candidate's status through the hiring pipeline.")

    records = get_all_candidates()

    if not records:
        st.info("No candidates tracked yet. Screen some resumes and click 'Save to Tracker'.")
    else:
        df = pd.DataFrame(records)
        df_display = df[
            ["id", "name", "email", "job_title", "final_score", "status", "applied_on"]
        ].rename(
            columns={
                "id": "ID",
                "name": "Name",
                "email": "Email",
                "job_title": "Job Title",
                "final_score": "Final Score",
                "status": "Status",
                "applied_on": "Applied On",
            }
        )

        edited_df = st.data_editor(
            df_display,
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status", options=STATUS_OPTIONS, required=True
                ),
                "ID": st.column_config.NumberColumn("ID", disabled=True),
            },
            disabled=["Name", "Email", "Job Title", "Final Score", "Applied On"],
            hide_index=True,
            use_container_width=True,
            key="tracker_editor",
        )

        if st.button("✅ Apply Status Changes"):
            for _, row in edited_df.iterrows():
                update_status(int(row["ID"]), row["Status"])
            st.success("Statuses updated!")
            st.rerun()

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Candidates Tracked", len(records))
        with col2:
            if st.button("🗑️ Clear All Tracked Records"):
                clear_all()
                st.rerun()
