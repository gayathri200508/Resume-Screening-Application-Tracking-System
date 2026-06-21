"""
cli.py
------
Optional command-line interface to screen and rank resumes without
launching the Streamlit UI. Handy for quick testing or for taking a
terminal screenshot for your report.

Usage:
    python cli.py --jd data/sample_job_description.txt --resumes data/sample_resumes/
"""

import argparse
import os

from src.resume_parser import extract_text, clean_text
from src.skill_extractor import extract_candidate_profile
from src.matcher import evaluate_resume, rank_candidates


def load_jd(jd_path: str) -> str:
    ext = os.path.splitext(jd_path)[1].lower()
    if ext == ".txt":
        with open(jd_path, "r", encoding="utf-8") as f:
            return clean_text(f.read())
    return clean_text(extract_text(jd_path))


def main():
    parser = argparse.ArgumentParser(description="Resume Screening & Ranking (CLI)")
    parser.add_argument("--jd", required=True, help="Path to job description (.txt/.pdf/.docx)")
    parser.add_argument("--resumes", required=True, help="Folder containing resume files")
    args = parser.parse_args()

    jd_text = load_jd(args.jd)

    resume_dir = args.resumes
    files = [
        os.path.join(resume_dir, f)
        for f in os.listdir(resume_dir)
        if f.lower().endswith((".pdf", ".docx"))
    ]

    if not files:
        print(f"No .pdf/.docx resumes found in: {resume_dir}")
        return

    results = []
    for path in files:
        text = clean_text(extract_text(path))
        profile = extract_candidate_profile(text)
        evaluation = evaluate_resume(text, jd_text)
        results.append(
            {
                "filename": os.path.basename(path),
                "name": profile["name"],
                "email": profile["email"],
                **evaluation,
            }
        )

    ranked = rank_candidates(results)

    print("\n" + "=" * 70)
    print(f"{'RANK':<5}{'NAME':<25}{'FINAL SCORE':<14}{'SIMILARITY':<12}{'SKILL MATCH'}")
    print("=" * 70)
    for i, c in enumerate(ranked, start=1):
        print(
            f"{i:<5}{c['name'][:24]:<25}{c['final_score']:<14}"
            f"{c['similarity_score']:<12}{c['skill_match_score']}"
        )
    print("=" * 70)

    print("\nTop candidate skill breakdown:")
    top = ranked[0]
    print(f"  Name           : {top['name']}")
    print(f"  Email          : {top['email']}")
    print(f"  Matched Skills : {', '.join(top['matched_skills']) or 'None'}")
    print(f"  Missing Skills : {', '.join(top['missing_skills']) or 'None'}")


if __name__ == "__main__":
    main()
