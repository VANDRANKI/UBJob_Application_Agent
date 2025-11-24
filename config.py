import os
from dotenv import load_dotenv

# Load environment variables from .env at project root
load_dotenv()

# CREDENTIALS
USERNAME = os.getenv("UB_USERNAME", "")
PASSWORD = os.getenv("UB_PASSWORD", "")
LOGIN_URL = os.getenv("UB_LOGIN_URL", "https://www.ubjobs.buffalo.edu/")

if not USERNAME or not PASSWORD:
    print("WARNING: UB_USERNAME or UB_PASSWORD not set in .env")
    
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
    "sponsorship_needed_in_future": "Yes",
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
            "major": "Mathematics, Physics & chemistry",
            "graduated": "Yes",
            "degree_type": "Other",
            "other_degree": "Intermediate College of Education"
        }
    ],

  # EMPLOYMENT -------------------------------------------------------
    "employment": [
        {
            "employer": "XXXXXXXX-University-of-Magic-Research",
            "phone": "1234567890",
            "address": "LOL-Street-Number-42",
            "city": "Faketown",
            "state": "ZZ",
            "begin_date": "99/99/9999",
            "end_date": "current Position",
            "title": "Ultra-Super-Duper-Research-Wizard",

            # EXACT DUTIES (WORD FOR WORD)
            "duties": (
                "Data Analysis & Optimization:\n"
                "- Did some top-secret xxxxxxxyyyyyyyy wizard-level data stuff.\n"
                "- Connected spooky dots between slurry goblins and planarization dragons.\n"
                "- Used reinforcement-learning-magic to make materials behave nicely.\n"
                "- Created a mega-database-of-doom that knows everything about CMP.\n\n"
                "AI & ML Research:\n"
                "- Built an AI pipeline so smart it almost asked for a salary.\n"
                "- NLP’d ceria synthesis papers until they begged for mercy.\n"
                "- Trained LLMs (OpenAI+++, MistralDragon, GeminiUltraLOL, SciBERT-on-Steroids).\n\n"
                "Worked on mysterious superhero-level projects with SamsungWizards Inc., MicronMagicians LLC, "
                "and created enough ML pipelines to make Skynet blush. Unlocked futuristic insights, "
                "optimized materials, and summoned AI agents that run on caffeine and chaos."
            ),

            "hours_per_week": "40",
            "supervisor": "Professor XXXXXXXXXY",
            "supervisor_title": "Supreme-Overlord-of-Science-and-Engineering",

            # EXACT REASON FOR LEAVING
            "reason_leaving": "Didn’t leave yet, but the contract ends on ZZZZ-date (yes, festive exit vibes).",

            "contact_employer": "Yes"
        },

        {
            "employer": "XXXXXXXX-University-of-Magic-Research",
            "phone": "1234567890",
            "address": "LOL-Street-Number-42",
            "city": "Faketown",
            "state": "ZZ",
            "begin_date": "88/88/8888",
            "end_date": "77/77/7777",
            "title": "Mini-Research-Wizard",

            "duties": (
                "Worked in the UltraCool Research Group, where I built a customized AI model that turns chaotic "
                "scientific literature into organized, obedient little datasets. Helped predict future experiments "
                "by convincing unstructured data to stop being dramatic."
            ),

            "hours_per_week": "20",
            "supervisor": "Professor XXXXXXXXXY",
            "supervisor_title": "Supreme-Overlord-of-Science-and-Engineering",
            "reason_leaving": "Student term ended and they hired me again because I'm awesome.",
            "contact_employer": "Yes"
        },

        {
            "employer": "XXXXXXXX-University-of-Magic-Research",
            "phone": "000-000-0000",
            "address": "LOL-Street-Number-42",
            "city": "Faketown",
            "state": "ZZ",
            "begin_date": "11/11/1111",
            "end_date": "22/22/2222",
            "title": "Teaching-Support-Wizard",

            "duties": (
                "Assisted in ML and Data Mining courses, guiding confused mortals with coding, concepts, and "
                "analysis sorcery. Helped students survive academic chaos using logic and caffeine."
            ),

            "hours_per_week": "20",
            "supervisor": "Professor YYYYYYYYY-ZZZZZZ",
            "supervisor_title": "Director of Wizardry and Applied Data Sorcery",
            "reason_leaving": "Classes ended, missions completed.",
            "contact_employer": "Yes"
        }
    ],

    # REFERENCES -------------------------------------------------------
    "references": [
        {
            "name": "Mr. Reference-Guy-XXXXXXXX",
            "email": "xxxxx@placeholder.com",
            "phone": "1111111111",
            "relationship": (
                "Met at multiple magical conferences where I presented scrolls of knowledge and battled with data."
            )
        },
        {
            "name": "Professor Reference-Y",
            "email": "yyyyy@placeholder.com",
            "phone": "2222222222",
            "relationship": (
                "Worked under him for two years learning secret research spells and publishing mystical papers."
            )
        },
        {
            "name": "Dr. ZZZZZ Reference-Woman",
            "email": "zzzzz@placeholder.com",
            "phone": "3333333333",
            "relationship": (
                "Collaborated on a academic project involving preprocessing dragons, mining goblins, "
                "and generating legendary final reports."
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
    "ASSOCIATE": os.path.join(RESUMES_DIR, "Resume_Associate.pdf")
}

# SETTINGS
HEADLESS = False # Set to True for production
CHECK_FREQUENCY_HOURS = 24
