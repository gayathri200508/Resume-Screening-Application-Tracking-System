"""
generate_sample_resumes.py
---------------------------
One-time helper script that generates a few sample resumes (DOCX + PDF)
into data/sample_resumes/ so graders/reviewers can run the project
immediately without needing their own resume files.

Run once with:
    python generate_sample_resumes.py
"""

import os
import docx
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

OUT_DIR = os.path.join("data", "sample_resumes")
os.makedirs(OUT_DIR, exist_ok=True)

RESUMES = [
    {
        "filename": "Aditi_Sharma.docx",
        "name": "Aditi Sharma",
        "lines": [
            "Aditi Sharma",
            "Email: aditi.sharma@example.com | Phone: 9876543210",
            "",
            "OBJECTIVE",
            "Aspiring Python Developer with strong fundamentals in backend "
            "development and databases, seeking an entry-level role.",
            "",
            "SKILLS",
            "Python, Django, Flask, SQL, MySQL, MongoDB, REST API, Git, GitHub, "
            "Data Structures, Algorithms, Object Oriented Programming, Agile, "
            "Problem Solving, Communication, Teamwork",
            "",
            "PROJECTS",
            "1. Built a REST API based library management system using Flask and MySQL.",
            "2. Developed a personal portfolio website using HTML, CSS and JavaScript.",
            "",
            "EDUCATION",
            "B.Tech in Computer Science, ABC University, 2026",
        ],
    },
    {
        "filename": "Rohan_Verma.docx",
        "name": "Rohan Verma",
        "lines": [
            "Rohan Verma",
            "Email: rohan.verma@example.com | Phone: 9123456780",
            "",
            "OBJECTIVE",
            "Final year Computer Science student interested in Data Science "
            "and Machine Learning roles.",
            "",
            "SKILLS",
            "Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL, "
            "Data Analysis, Data Visualization, Communication, Teamwork",
            "",
            "PROJECTS",
            "1. Built a movie recommendation system using Machine Learning.",
            "2. Performed data analysis on sales data using Pandas and Matplotlib.",
            "",
            "EDUCATION",
            "B.Tech in Computer Science, XYZ University, 2026",
        ],
    },
    {
        "filename": "Sneha_Iyer.pdf",
        "name": "Sneha Iyer",
        "lines": [
            "Sneha Iyer",
            "Email: sneha.iyer@example.com | Phone: 9988776655",
            "",
            "OBJECTIVE",
            "Software engineering graduate skilled in full-stack web development.",
            "",
            "SKILLS",
            "Java, JavaScript, React, Node.js, HTML, CSS, SQL, Git, Agile, "
            "Problem Solving, Leadership",
            "",
            "PROJECTS",
            "1. Developed an e-commerce website using React and Node.js.",
            "2. Built a chat application using JavaScript and Firebase.",
            "",
            "EDUCATION",
            "B.E in Information Technology, PQR College, 2026",
        ],
    },
]


def make_docx(resume):
    path = os.path.join(OUT_DIR, resume["filename"])
    document = docx.Document()
    for line in resume["lines"]:
        document.add_paragraph(line)
    document.save(path)
    print(f"Created {path}")


def make_pdf(resume):
    path = os.path.join(OUT_DIR, resume["filename"])
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    y = height - 60
    for line in resume["lines"]:
        c.drawString(60, y, line)
        y -= 18
        if y < 60:
            c.showPage()
            y = height - 60
    c.save()
    print(f"Created {path}")


if __name__ == "__main__":
    for r in RESUMES:
        if r["filename"].endswith(".docx"):
            make_docx(r)
        else:
            make_pdf(r)
    print("\nSample resumes generated in data/sample_resumes/")
