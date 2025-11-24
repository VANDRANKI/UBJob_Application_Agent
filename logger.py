import os
import pandas as pd
from datetime import datetime
from .config import LOGS_DIR

LOG_FILE = os.path.join(LOGS_DIR, "jobs_log.csv")

def init_log():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=[
            "Date_Discovered", "Job_ID", "Job_Title", "Department", 
            "Resume_Type", "Status", "Submission_Date", "Confirmation_Num", 
            "Deadline", "Notes"
        ])
        df.to_csv(LOG_FILE, index=False)

def log_job(job_data):
    init_log()
    df = pd.read_csv(LOG_FILE)
    
    # Check if job already exists
    if str(job_data["Job_ID"]) in df["Job_ID"].astype(str).values:
        return False # Already logged
        
    new_row = {
        "Date_Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Job_ID": job_data.get("Job_ID"),
        "Job_Title": job_data.get("Job_Title"),
        "Department": job_data.get("Department"),
        "Resume_Type": job_data.get("Resume_Type", "Pending"),
        "Status": "Pending",
        "Submission_Date": "",
        "Confirmation_Num": "",
        "Deadline": job_data.get("Deadline", ""),
        "Notes": job_data.get("Notes", "")
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    return True

def update_status(job_id, status, notes=""):
    init_log()
    df = pd.read_csv(LOG_FILE)
    mask = df["Job_ID"].astype(str) == str(job_id)
    if mask.any():
        df.loc[mask, "Status"] = status
        if notes:
            df.loc[mask, "Notes"] = notes
        if status == "Submitted":
            df.loc[mask, "Submission_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(LOG_FILE, index=False)
