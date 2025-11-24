import re

# KEYWORDS DEFINITION
KEYWORDS = {
    "DATA": {
        "role_types": [
            "Data Analyst", "Data Scientist", "Data Engineer", "Business Intelligence",
            "Analytics Specialist", "Visualization Specialist", "Machine Learning",
            "Quantitative", "Statistical", "Database Analyst"
        ],
        "skills": [
            "Python", "SQL", "R", "Tableau", "Power BI", "data modeling", "data analysis", "NLP",
            "deep learning", "data visualization", "big data", "Hadoop", "Spark", "data cleaning",
            "statistical analysis", "machine learning", "data pipelines", "ETL", "ML", "DL", "NN",
            "artificial intelligence", "AI", "data science", "predictive modeling",
            "data warehousing", "predictive analytics", "data mining", "visualization"
        ]
    },
    "RESEARCH": {
        "role_types": [
            "Research Associate", "Research Scientist", "Materials Scientist", "Academic Researcher",
            "Research Engineer",  "Research Fellow",
            "Chemical Engineer", "Laboratory Technician", "Postdoctoral",
            "Research Specialist", "Technical Specialist", "Process Engineer",
            "Quality Engineer"
        ],
        "skills": [
            "materials science", "nanotechnology", "CMP", "chemical mechanical planarization",
            "laboratory", "experimental design", "characterization", "microscopy", "Slurry Analysis",
            "XRD", "SEM", "TEM", "AFM", "data analysis",
            "synthesis", "process optimization", "publications", "life cycle assessment",
            "sustainability"
        ]
    },
    "Associate": {
        "role_types": [
            "Program Associate", "Project Coordinator", "Administrative", "Office Analyst", "Donar Analyst",
            "Operations Associate", "Technical Support", "Program Manager", "Database Coordinator",
            "Research Administrator", "Academic Advisor", "Student Services",
            "Grant Writer"
        ],
        "skills": [
            "project management", "coordination", "administration", "stakeholder", "analyst", "communication",
            "documentation", "process improvement", "support services", "Office Analysis", "Excel Engineer",
            "program development", "grant administration"
        ]
    }
}

def normalize_text(text):
    return text.lower()

def count_matches(text, keywords):
    count = 0
    text = normalize_text(text)
    for kw in keywords:
        if normalize_text(kw) in text:
            count += 1
    return count

def determine_resume_type(job_title, job_description):
    scores = {"DATA": 0, "RESEARCH": 0, "ASSOCIATE": 0}
    
    # 1. Check Role Title Matches (High Weight)
    for category, data in KEYWORDS.items():
        if count_matches(job_title, data["role_types"]) > 0:
            scores[category] += 10 # High priority for title match
            
    # 2. Check Description Keywords
    for category, data in KEYWORDS.items():
        scores[category] += count_matches(job_description, data["skills"])
        
    # Determine winner
    best_category = max(scores, key=scores.get)
    
    # If no matches at all, default to Associate (Resume 3) as per prompt
    if scores[best_category] == 0:
        return "Associate"
        
    return best_category
