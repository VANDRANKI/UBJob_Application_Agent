import os

# CREDENTIALS
USERNAME = "Prabhu_Kiran"
PASSWORD = "BCTRXa_x*kE2Qia"
LOGIN_URL = "https://www.ubjobs.buffalo.edu/"

# PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
RESUMES_DIR = os.path.join(BASE_DIR, "resumes")
GENERATED_DOCS_DIR = os.path.join(BASE_DIR, "generated_docs")

# Ensure directories exist
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(GENERATED_DOCS_DIR, exist_ok=True)

# USER DATA
PERSONAL_INFO = {
    # BASIC INFO
    "first_name": "Prabhu Kiran",
    "last_name": "Vandranki",
    "preferred_name": "Prabhu",
    "pronouns": "He/Him",
    "email": "vandrap@clarkson.edu",
    "phone": "3156033719",

    "address": "Apt 2-4, 200 Main Street, Potsdam Main Street Apartments",
    "city": "Potsdam",
    "state": "NY",
    "zip_code": "13676",
    "country": "United States of America",

    "authorized_to_work": "Yes",
    "over_18": "Yes",
    "previous_ub_affiliation": "No",

    # EDUCATION --------------------------------------------------------
    "education": [
        {
            "school": "Clarkson University",
            "major": "Applied Data Science & Information Visualization",
            "graduated": "Yes",
            "degree_type": "Masters",
            "other_degree": "Master of Science(MSc) Data Science"
        },
        {
            "school": "Parul University",
            "major": "Computer Science & Machine Learning Engineering",
            "graduated": "Yes",
            "degree_type": "Bachelors",
            "other_degree": "Bachelor of Technology (B.Tech) In CSE"
        },
        {
            "school": "Narayana Junior College",
            "major": "Mathematics, Accounting, Physics & chemistry",
            "graduated": "Yes",
            "degree_type": "Other",
            "other_degree": "Intermediate College of Education"
        }
    ],

    # EMPLOYMENT -------------------------------------------------------
    "employment": [
        {
            "employer": "Clarkson University",
            "phone": "3152682289",
            "address": "8 Clarkson Ave",
            "city": "Potsdam",
            "state": "NY",
            "begin_date": "05/06/2025",
            "end_date": "current Position",
            "title": "Visiting Research Associate",

            # EXACT DUTIES (WORD FOR WORD)
            "duties": (
                "Data Analysis & Optimization:\n"
                "- Performed large-scale statistical and correlation analysis of text-mined data points.\n"
                "- Uncovered robust relationships between slurry variables, process settings, and planarization outcomes.\n"
                "- Applied deep reinforcement learning to CMP slurry formulations for better selectivity, lower defect rates, and higher removal rates.\n"
                "- Established a unified database for CMP literature, enabling evidence-based slurry optimization and new pattern discovery.\n\n"
                "AI & ML Research:\n"
                "- Designed and deployed an AI-agent-driven literature mining pipeline that scraped and organized data from 300+ CMP (Chemical Mechanical Planarization) research papers.\n"
                "- Built NLP workflows to automatically extract ceria synthesis conditions, slurry chemistry, particle processing parameters, and performance metrics.\n"
                "- Developed structured JSON datasets and trained custom LLMs (like OpenAI, Mistral, Gemini, SciBERT) for automated scientific knowledge extraction.\n\n"
                "Worked on multiple projects including CU-DFT data analysis and model development for Samsung company (this work published in Corrosion Science), and ceria synthesis/slurry optimization for CMP. Extended this research to sustainability and life-cycle assessment (LCA) in collaboration with Micron company. Built a database and deployed advanced ML models and applications, LLMs, and AI agents to drive data-driven insights, optimize processes, and support innovative materials research."
            ),

            "hours_per_week": "40",
            "supervisor": "Dr. Jihoon Seo",
            "supervisor_title": "Professor(Department Of Chemical & Biomolecular Engineering)",

            # EXACT REASON FOR LEAVING
            "reason_leaving": "Didn’t left yet, but my contract is ending this December 25th 2025, (yep, a very festive offboarding date)",

            "contact_employer": "Yes"
        },

        {
            "employer": "Clarkson University",
            "phone": "3152682289",
            "address": "8 Clarkson Ave",
            "city": "Potsdam",
            "state": "NY",
            "begin_date": "09/16/2024",
            "end_date": "05/08/2025",
            "title": "Research Assistant",

            "duties": (
                "Worked in Seo Research Group, where i have developed a customized expert model and applications to process "
                "and analyze scientific literature on ceria synthesis in the CMP domain. Enabled prediction of future synthesis "
                "and experiments by turning unstructured data into actionable insights, supporting data-driven decisions to "
                "optimize material synthesis and experimental conditions."
            ),

            "hours_per_week": "20",
            "supervisor": "Dr. Jihoon Seo",
            "supervisor_title": "Professor(Department Of Chemical & Biomolecular Engineering)",
            "reason_leaving": "My term Ended as a student in Clarkson University and I got the job again on the same SEO Research Group Lab as a Visiting Research Associate",
            "contact_employer": "Yes"
        },

        {
            "employer": "Clarkson University",
            "phone": "315-268-6400",
            "address": "8 Clarkson Ave",
            "city": "Potsdam",
            "state": "NY",
            "begin_date": "04/17/2024",
            "end_date": "09/23/2024",
            "title": "Graduate Assistant",

            "duties": (
                "Assisted in Machine Learning (IA651) and Data Mining (IA650) courses, providing support in "
                "lectures, assignments, and research projects. Guided students with concepts, coding, and analysis, "
                "while contributing expertise to enhance learning outcomes and project success."
            ),

            "hours_per_week": "20",
            "supervisor": "Dr. Brois Jukic",
            "supervisor_title": "Professor at Clarkson University and Masters Applied Data Science Director",
            "reason_leaving": "The projects and the classes ended there.",
            "contact_employer": "Yes"
        }
    ],

    # REFERENCES -------------------------------------------------------
    "references": [
        {
            "name": "Arunkumar Venkataronappa",
            "email": "arunkumargv@ibm.com",
            "phone": "3152444165",
            "relationship": (
                "I have met him at multiple conferences, including the CMPUG Conference held at Lewis University "
                "in Chicago, Illinois; the CAMP CMP Conference in Saratoga; and the CAMP Technical Conference "
                "in Geneva, where I presented my posters and project work."
            )
        },
        {
            "name": "Jihoon Seo",
            "email": "jseo@clarkson.edu",
            "phone": "3152682289",
            "relationship": (
                "I have worked under him for two years, first as a research assistant and currently as a visiting "
                "research associate in his lab. During this time, we have completed multiple projects and published "
                "two papers: one in Corrosion Science and another in Micron (MDPI)."
            )
        },
        {
            "name": "Sumona Mondal",
            "email": "smondal@clarkson.edu",
            "phone": "3152686415",
            "relationship": (
                "I collaborated with her on a comprehensive data mining project, where I was responsible for tasks "
                "such as data preprocessing, exploratory analysis, and applying appropriate mining techniques. "
                "Together, we successfully completed the project and produced a detailed final report documenting "
                "the methodology, findings, and recommendations."
            )
        }
    ],

    # EEO --------------------------------------------------------------
    "eeo": {
        "gender": "Male",
        "ethnicity": "Not Hispanic or Latino",
        "race": "Asian",
        "race_sub": "Asian Indian",
        "language": "English, Other",
        "lgbtq": "No"
    },

    # DISABILITY & VETERAN STATUS --------------------------------------
    "disability_status": "No, I do not have a disability and have not had one in the past",
    "veteran_status": "I am not a protected veteran",
}

# RESUME PATHS (Placeholders)
RESUME_PATHS = {
    "DATA": os.path.join(RESUMES_DIR, "Resume_Data.pdf"),
    "RESEARCH": os.path.join(RESUMES_DIR, "Resume_Research.pdf"),
    "ADMIN": os.path.join(RESUMES_DIR, "Resume_Admin.pdf")
}

# SETTINGS
HEADLESS = False # Set to True for production
CHECK_FREQUENCY_HOURS = 24
